# Experimentation

## Objective

Estimate the causal impact of different free shipping thresholds using a randomized A/B/n experiment.

---

## When to Use A/B Testing

Appropriate because:

- We can randomize traffic
- The effect (conversion + margin) is measurable quickly
- Risk is controlled via guardrails

---

## Core Components

### 1. Hypothesis

- Lower threshold ($35):
  - ↑ Conversion
  - ↓ AOV
  - ↑ Shipping subsidy
  - ↓ Contribution margin

- Higher threshold ($65):
  - ↓ Conversion
  - ↑ AOV
  - ↓ Shipping subsidy
  - Net effect uncertain

---

### 2. Metrics

**Primary:**
- Contribution Margin per Session

**Secondary:**
- Conversion rate
- Average order value (AOV)
- Revenue per session

**Guardrails:**
- Shipping subsidy per order
- Negative margin order rate
- Revenue per session

---

### 3. Power & Sample Size

- MDE ≈ $0.025 CM/session (~9%)
- Sample size ≈ 150,000 sessions per arm
- Runtime ≈ 45 days
- Power = 80%, Alpha = 0.05

---

### 4. Randomization

- Session-level randomization
- Balanced traffic across arms
- SRM test passed (no imbalance detected)

---

### 5. Evaluation

- Compare treatment vs baseline ($50)
- Use:
  - mean differences
  - confidence intervals
  - t-tests

---

## Result Summary

- $35 → significantly worse
- $65 → slightly higher CM but not significant
- $50 → best overall balance

---

## Heuristic

If the result does not change a decision (e.g., $65 vs $50), do not roll out.