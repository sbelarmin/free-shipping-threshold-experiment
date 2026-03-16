from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
import pandas as pd
import yaml

try:
    from scipy.stats import chisquare
except Exception:  # pragma: no cover
    chisquare = None


# =========================================================
# Configuration
# =========================================================

@dataclass
class Paths:
    config_path: Path = Path("configs/experiment_config.yaml")
    output_dir: Path = Path("data/synthetic")
    output_file: str = "free_shipping_experiment_sessions.csv"


# =========================================================
# Helpers
# =========================================================

def load_config(path: str | Path) -> Dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def clipped_normal(
    mean: float,
    std: float,
    size: int,
    lower: float,
    upper: float | None,
    rng: np.random.Generator,
) -> np.ndarray:
    """Sample from a normal distribution and clip to bounds."""
    values = rng.normal(loc=mean, scale=std, size=size)
    if upper is None:
        return np.clip(values, lower, None)
    return np.clip(values, lower, upper)


def estimate_visitor_pool_size(
    calendar_df: pd.DataFrame,
    avg_sessions_per_day: int,
    avg_sessions_per_visitor: float = 3.0,
) -> int:
    estimated_total_sessions = len(calendar_df) * avg_sessions_per_day
    return max(int(np.ceil(estimated_total_sessions / avg_sessions_per_visitor)), 50_000)


# =========================================================
# 1) Calendar
# =========================================================

def generate_calendar(config: Dict) -> pd.DataFrame:
    dates_cfg = config["experiment_dates"]

    start_date = pd.to_datetime(dates_cfg["pre_period_start"])
    test_start = pd.to_datetime(dates_cfg["test_start"])
    test_end = pd.to_datetime(dates_cfg["test_end"])

    session_dates = pd.date_range(start=start_date, end=test_end, freq="D")
    calendar_df = pd.DataFrame({"session_date": session_dates})
    calendar_df["period"] = np.where(calendar_df["session_date"] < test_start, "pre", "test")
    calendar_df["is_test_period"] = calendar_df["period"].eq("test")
    return calendar_df


# =========================================================
# 2) Visitors
# =========================================================

def generate_visitors(
    n_visitors: int,
    config: Dict,
    rng: np.random.Generator,
) -> pd.DataFrame:
    # Region mix can be expanded later; keeping simple and realistic.
    region_names = ["West", "Central", "East", "South"]
    region_probs = [0.30, 0.25, 0.25, 0.20]

    experiment_arms = list(config["experiment"]["arms"].keys())
    arm_probs = [1 / len(experiment_arms)] * len(experiment_arms)

    visitors = pd.DataFrame({
        "visitor_id": np.arange(1, n_visitors + 1, dtype=np.int64),
        "region": rng.choice(region_names, size=n_visitors, p=region_probs),
        # persistent test-period assignment at visitor level
        "test_arm": rng.choice(experiment_arms, size=n_visitors, p=arm_probs),
        # latent heterogeneity so data feels less synthetic
        "conversion_multiplier": np.clip(rng.lognormal(mean=0.0, sigma=0.20, size=n_visitors), 0.6, 1.5),
        "basket_multiplier": np.clip(rng.lognormal(mean=0.0, sigma=0.15, size=n_visitors), 0.7, 1.4),
    })
    return visitors


# =========================================================
# 3) Sessions
# =========================================================

def generate_sessions(
    calendar_df: pd.DataFrame,
    visitors_df: pd.DataFrame,
    config: Dict,
    rng: np.random.Generator,
) -> pd.DataFrame:
    avg_sessions_per_day = int(config["traffic"]["avg_sessions_per_day"])
    session_std_dev = int(config["traffic"].get("session_std_dev", 0))

    visitor_ids = visitors_df["visitor_id"].to_numpy()
    sessions = []
    session_counter = 1

    for _, row in calendar_df.iterrows():
        if session_std_dev > 0:
            n_sessions = int(np.round(rng.normal(avg_sessions_per_day, session_std_dev)))
            n_sessions = max(n_sessions, 100)
        else:
            n_sessions = avg_sessions_per_day

        sampled_visitors = rng.choice(visitor_ids, size=n_sessions, replace=True)

        day_sessions = pd.DataFrame({
            "session_id": np.arange(session_counter, session_counter + n_sessions, dtype=np.int64),
            "visitor_id": sampled_visitors,
            "session_date": row["session_date"],
            "period": row["period"],
        })
        sessions.append(day_sessions)
        session_counter += n_sessions

    sessions_df = pd.concat(sessions, ignore_index=True)
    return sessions_df


# =========================================================
# 4) Assign experiment arms
# =========================================================

def assign_experiment_arms(
    sessions_df: pd.DataFrame,
    visitors_df: pd.DataFrame,
) -> pd.DataFrame:
    df = sessions_df.merge(
        visitors_df[["visitor_id", "region", "test_arm", "conversion_multiplier", "basket_multiplier"]],
        on="visitor_id",
        how="left",
    )

    df["threshold_arm"] = np.where(df["period"].eq("pre"), "pre", df["test_arm"])

    threshold_map = {
        "pre": 50,
        "t35": 35,
        "t50": 50,
        "t65": 65,
    }
    df["free_shipping_threshold"] = df["threshold_arm"].map(threshold_map).astype(float)
    return df


# =========================================================
# 5) Simulate conversion
# =========================================================

def simulate_conversion(
    df: pd.DataFrame,
    config: Dict,
    rng: np.random.Generator,
) -> pd.DataFrame:
    # pre-period uses business-as-usual = t50
    base_rates = {
        "pre": config["experiment"]["arms"]["t50"]["conversion_rate"],
        "t35": config["experiment"]["arms"]["t35"]["conversion_rate"],
        "t50": config["experiment"]["arms"]["t50"]["conversion_rate"],
        "t65": config["experiment"]["arms"]["t65"]["conversion_rate"],
    }

    df["base_conversion_rate"] = df["threshold_arm"].map(base_rates).astype(float)
    df["conversion_probability"] = np.clip(
        df["base_conversion_rate"] * df["conversion_multiplier"],
        0.0001,
        0.25,
    )

    df["converted"] = (
        rng.random(len(df)) < df["conversion_probability"].to_numpy()
    ).astype(int)

    return df


# =========================================================
# 6) Revenue generation logic
# =========================================================

def _solve_above_threshold_mean(
    target_aov: float,
    qualification_rate: float,
    threshold: float,
    below_fraction_of_threshold: float = 0.82,
) -> float:
    """
    Solve for mean above-threshold revenue so the mixture roughly matches target AOV.
    target_aov = q * mean_above + (1-q) * mean_below
    mean_below = below_fraction_of_threshold * threshold
    """
    q = qualification_rate
    mean_below = below_fraction_of_threshold * threshold
    if q <= 0:
        return target_aov
    mean_above = (target_aov - (1 - q) * mean_below) / q
    return max(mean_above, threshold + 2.0)


def _draw_product_revenue_for_arm(
    n_orders: int,
    threshold: float,
    target_aov: float,
    qualification_rate: float,
    basket_multiplier: np.ndarray,
    rng: np.random.Generator,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Returns:
        qualified_for_free_shipping (0/1)
        product_revenue
    """
    qualifies = (rng.random(n_orders) < qualification_rate).astype(int)

    below_fraction = 0.82
    below_mean = below_fraction * threshold
    above_mean = _solve_above_threshold_mean(
        target_aov=target_aov,
        qualification_rate=qualification_rate,
        threshold=threshold,
        below_fraction_of_threshold=below_fraction,
    )

    below_std = max(threshold * 0.10, 2.5)
    above_std = max(threshold * 0.12, 3.0)

    product_revenue = np.empty(n_orders, dtype=float)

    # below-threshold orders
    below_idx = np.where(qualifies == 0)[0]
    if len(below_idx) > 0:
        below_vals = clipped_normal(
            mean=below_mean,
            std=below_std,
            size=len(below_idx),
            lower=5.0,
            upper=threshold - 0.01,
            rng=rng,
        )
        product_revenue[below_idx] = below_vals

    # above-threshold orders
    above_idx = np.where(qualifies == 1)[0]
    if len(above_idx) > 0:
        above_vals = clipped_normal(
            mean=above_mean,
            std=above_std,
            size=len(above_idx),
            lower=threshold,
            upper=None,
            rng=rng,
        )
        product_revenue[above_idx] = above_vals

    # apply visitor-level basket heterogeneity
    product_revenue = product_revenue * basket_multiplier
    product_revenue = np.clip(product_revenue, 5.0, None)

    return qualifies, product_revenue


# =========================================================
# 7) Orders + shipping logic + economics
# =========================================================

def simulate_orders_and_financials(
    df: pd.DataFrame,
    config: Dict,
    rng: np.random.Generator,
) -> pd.DataFrame:
    economics = config["economics"]
    basket_cfg = config["basket_model"]
    arms_cfg = config["experiment"]["arms"]

    shipping_cost_per_order = float(economics["shipping_cost_per_order"])
    shipping_fee_if_not_qualified = float(economics["shipping_fee_if_not_qualified"])
    cogs_ratio = float(economics["cogs_ratio"])

    # initialize columns for all sessions
    df["order_id"] = pd.Series([None] * len(df), dtype="object")
    df["units"] = 0
    df["price_per_unit"] = 0.0
    df["product_revenue"] = 0.0
    df["shipping_revenue"] = 0.0
    df["total_revenue"] = 0.0
    df["cogs"] = 0.0
    df["shipping_cost"] = 0.0
    df["contribution_margin"] = 0.0
    df["qualified_for_free_shipping"] = 0

    converted_idx = df.index[df["converted"] == 1]
    if len(converted_idx) == 0:
        return df

    converted = df.loc[converted_idx].copy()

    # units per order
    avg_units = float(basket_cfg["avg_units_per_order"])
    units_std = float(basket_cfg.get("units_std_dev", 1.0))

    # simple rounded normal to get realistic integers
    units = np.round(rng.normal(loc=avg_units, scale=units_std, size=len(converted))).astype(int)
    units = np.clip(units, 1, 8)
    converted["units"] = units

    # revenue generation by arm
    for arm in ["pre", "t35", "t50", "t65"]:
        arm_mask = converted["threshold_arm"] == arm
        if arm_mask.sum() == 0:
            continue

        if arm == "pre":
            arm_params = arms_cfg["t50"]
        else:
            arm_params = arms_cfg[arm]

        threshold = float(converted.loc[arm_mask, "free_shipping_threshold"].iloc[0])
        target_aov = float(arm_params["target_aov"])
        q_rate = float(arm_params["free_shipping_qualification_rate"])

        basket_mult = converted.loc[arm_mask, "basket_multiplier"].to_numpy()

        qualifies, product_revenue = _draw_product_revenue_for_arm(
            n_orders=arm_mask.sum(),
            threshold=threshold,
            target_aov=target_aov,
            qualification_rate=q_rate,
            basket_multiplier=basket_mult,
            rng=rng,
        )

        # derive price per unit from product revenue
        arm_units = converted.loc[arm_mask, "units"].to_numpy()
        price_per_unit = product_revenue / arm_units
        price_per_unit = np.round(price_per_unit, 2)
        product_revenue = np.round(price_per_unit * arm_units, 2)

        shipping_revenue = np.where(qualifies == 1, 0.0, shipping_fee_if_not_qualified)
        shipping_cost = np.full(shape=arm_mask.sum(), fill_value=shipping_cost_per_order)
        cogs = np.round(product_revenue * cogs_ratio, 2)
        total_revenue = np.round(product_revenue + shipping_revenue, 2)
        contribution_margin = np.round(total_revenue - cogs - shipping_cost, 2)

        converted.loc[arm_mask, "qualified_for_free_shipping"] = qualifies.astype(int)
        converted.loc[arm_mask, "price_per_unit"] = price_per_unit
        converted.loc[arm_mask, "product_revenue"] = product_revenue
        converted.loc[arm_mask, "shipping_revenue"] = shipping_revenue
        converted.loc[arm_mask, "shipping_cost"] = shipping_cost
        converted.loc[arm_mask, "cogs"] = cogs
        converted.loc[arm_mask, "total_revenue"] = total_revenue
        converted.loc[arm_mask, "contribution_margin"] = contribution_margin

    # assign order ids
    converted["order_id"] = [f"O{i:09d}" for i in range(1, len(converted) + 1)]

    # write back
    cols_to_update = [
        "order_id",
        "units",
        "price_per_unit",
        "product_revenue",
        "shipping_revenue",
        "total_revenue",
        "cogs",
        "shipping_cost",
        "contribution_margin",
        "qualified_for_free_shipping",
    ]
    df.loc[converted_idx, cols_to_update] = converted[cols_to_update]

    return df


# =========================================================
# 8) Summaries
# =========================================================

def summarize_experiment(df: pd.DataFrame) -> pd.DataFrame:
    test_df = df[df["period"] == "test"].copy()

    summary = (
        test_df.groupby("threshold_arm", as_index=False)
        .agg(
            sessions=("session_id", "count"),
            orders=("converted", "sum"),
            product_revenue=("product_revenue", "sum"),
            shipping_revenue=("shipping_revenue", "sum"),
            total_revenue=("total_revenue", "sum"),
            cogs=("cogs", "sum"),
            shipping_cost=("shipping_cost", "sum"),
            contribution_margin=("contribution_margin", "sum"),
            free_shipping_orders=("qualified_for_free_shipping", "sum"),
            negative_margin_orders=("contribution_margin", lambda s: int((s < 0).sum())),
        )
    )

    summary["conversion_rate"] = summary["orders"] / summary["sessions"]
    summary["aov"] = np.where(summary["orders"] > 0, summary["product_revenue"] / summary["orders"], 0.0)
    summary["revenue_per_session"] = summary["total_revenue"] / summary["sessions"]
    summary["cm_per_session"] = summary["contribution_margin"] / summary["sessions"]
    summary["free_shipping_qualification_rate"] = np.where(
        summary["orders"] > 0, summary["free_shipping_orders"] / summary["orders"], 0.0
    )
    summary["shipping_subsidy_per_order"] = np.where(
        summary["orders"] > 0,
        (summary["shipping_cost"] - summary["shipping_revenue"]) / summary["orders"],
        0.0,
    )
    summary["negative_margin_order_rate"] = np.where(
        summary["orders"] > 0,
        summary["negative_margin_orders"] / summary["orders"],
        0.0,
    )

    metric_order = [
        "threshold_arm",
        "sessions",
        "orders",
        "conversion_rate",
        "aov",
        "revenue_per_session",
        "cm_per_session",
        "free_shipping_qualification_rate",
        "shipping_subsidy_per_order",
        "negative_margin_order_rate",
    ]
    return summary[metric_order].sort_values("threshold_arm").reset_index(drop=True)


# =========================================================
# 9) Diagnostics
# =========================================================

def run_diagnostics(df: pd.DataFrame) -> Dict:
    diagnostics = {}

    test_df = df[df["period"] == "test"].copy()

    # SRM on sessions by arm
    observed = test_df["threshold_arm"].value_counts().reindex(["t35", "t50", "t65"], fill_value=0)
    diagnostics["observed_sessions_by_arm"] = observed.to_dict()

    if chisquare is not None:
        expected = np.repeat(observed.sum() / 3, 3)
        stat, p_value = chisquare(f_obs=observed.to_numpy(), f_exp=expected)
        diagnostics["srm_chi_square_stat"] = float(stat)
        diagnostics["srm_p_value"] = float(p_value)
    else:
        diagnostics["srm_chi_square_stat"] = None
        diagnostics["srm_p_value"] = None

    # visitor consistency: each visitor should be in one arm in test
    visitor_arm_counts = test_df.groupby("visitor_id")["threshold_arm"].nunique()
    inconsistent_visitors = int((visitor_arm_counts > 1).sum())
    diagnostics["inconsistent_test_assignments"] = inconsistent_visitors

    # business-rule checks
    converted = df[df["converted"] == 1].copy()
    shipping_logic_ok = (
        ((converted["qualified_for_free_shipping"] == 1) & (converted["shipping_revenue"] == 0.0))
        | ((converted["qualified_for_free_shipping"] == 0) & (converted["shipping_revenue"] > 0.0))
    ).all()
    diagnostics["shipping_logic_valid"] = bool(shipping_logic_ok)

    total_revenue_ok = np.allclose(
        converted["total_revenue"].to_numpy(),
        (converted["product_revenue"] + converted["shipping_revenue"]).to_numpy(),
        atol=0.01,
    )
    diagnostics["total_revenue_formula_valid"] = bool(total_revenue_ok)

    cm_ok = np.allclose(
        converted["contribution_margin"].to_numpy(),
        (converted["total_revenue"] - converted["cogs"] - converted["shipping_cost"]).to_numpy(),
        atol=0.01,
    )
    diagnostics["contribution_margin_formula_valid"] = bool(cm_ok)

    return diagnostics


# =========================================================
# 10) Save
# =========================================================

def save_dataset(df: pd.DataFrame, paths: Paths) -> Path:
    ensure_output_dir(paths.output_dir)
    output_path = paths.output_dir / paths.output_file
    df.to_csv(output_path, index=False)
    return output_path


# =========================================================
# Main
# =========================================================

def main(seed: int = 42) -> None:
    rng = np.random.default_rng(seed)
    paths = Paths()

    config = load_config(paths.config_path)

    calendar_df = generate_calendar(config)

    n_visitors = estimate_visitor_pool_size(
        calendar_df=calendar_df,
        avg_sessions_per_day=int(config["traffic"]["avg_sessions_per_day"]),
        avg_sessions_per_visitor=3.0,
    )
    visitors_df = generate_visitors(n_visitors=n_visitors, config=config, rng=rng)

    sessions_df = generate_sessions(calendar_df, visitors_df, config, rng)
    assigned_df = assign_experiment_arms(sessions_df, visitors_df)
    converted_df = simulate_conversion(assigned_df, config, rng)
    final_df = simulate_orders_and_financials(converted_df, config, rng)

    output_path = save_dataset(final_df, paths)
    summary_df = summarize_experiment(final_df)
    diagnostics = run_diagnostics(final_df)

    print("\nSaved dataset:")
    print(output_path)

    print("\nExperiment summary (test period):")
    print(summary_df.to_string(index=False))

    print("\nDiagnostics:")
    for k, v in diagnostics.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()