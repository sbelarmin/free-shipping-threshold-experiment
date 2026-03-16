# Free Shipping Threshold Experiment — Result Review

This section reviews the synthetic experiment results using the same framework typically used by experimentation teams at companies like **Google, Airbnb, Netflix, and Meta**.

The review proceeds in the following order:

1. Diagnostics (experiment health)  
2. Primary metric evaluation  
3. Mechanism metrics  
4. Guardrail metrics  
5. Decision rule application  

---

# 1. Diagnostics (Experiment Health)

The first step in any experiment review is verifying that the experiment ran correctly.

The key question is:

> Can we trust the data?

## Sample Ratio Mismatch (SRM)

Expected traffic allocation:

| Arm | Expected Sessions |
| --- | ----------------- |
| t35 | ~150,000          |
| t50 | ~150,000          |
| t65 | ~150,000          |

Observed sessions:

| Arm | Sessions |
| --- | -------- |
| t35 | 149,618  |
| t50 | 150,306  |
| t65 | 149,618  |

SRM test result:

```
p-value = 0.3489
```

Interpretation:

- p-value > 0.05  
- traffic allocation appears random  
- **no SRM detected**

This indicates the experiment assignment system behaved correctly.

---

## Visitor Assignment Consistency

```
inconsistent_test_assignments: 0
```

Meaning:

- each visitor saw only one threshold  
- visitor-level randomization worked correctly  

---

## Data Logic Validation

All validation checks passed:

```
shipping_logic_valid: True
total_revenue_formula_valid: True
contribution_margin_formula_valid: True
```

This confirms:

- shipping rules were applied correctly  
- revenue formulas are correct  
- contribution margin calculations are correct  

These checks must pass before interpreting experiment results.

---

# 2. Primary Metric Review

The primary decision metric is:

```
Contribution Margin per Session
```

Results:

| Arm | CM per Session |
| --- | -------------- |
| t35 | 0.232          |
| t50 | 0.332          |
| t65 | 0.334          |

Interpretation:

- **t35 performs substantially worse**
- **t50 and t65 perform similarly**
- **t65 is slightly higher**

Difference between the top two arms:

```
t65 - t50 ≈ +0.002
```

This difference is extremely small.

In a real experiment review, the immediate question would be:

> Is this difference statistically significant or economically meaningful?

Most likely, this difference is **not economically meaningful**.

---

# 3. Mechanism Metrics

Mechanism metrics help explain **why the experiment produced these results**.

---

## Conversion Rate

| Arm | Conversion Rate |
| --- | --------------- |
| t35 | 2.21%           |
| t50 | 2.05%           |
| t65 | 1.75%           |

Interpretation:

Lower shipping thresholds reduce checkout friction and increase conversion.

Observed pattern matches expectations.

---

## Average Order Value (AOV)

| Arm | AOV  |
| --- | ---- |
| t35 | 44.4 |
| t50 | 55.4 |
| t65 | 60.0 |

Interpretation:

Higher thresholds encourage customers to add items to qualify for free shipping.

Observed pattern matches expectations.

---

## Revenue per Session

| Arm | Revenue per Session |
| --- | ------------------- |
| t35 | 1.02                |
| t50 | 1.20                |
| t65 | 1.12                |

Interpretation:

- t35 loses revenue due to smaller baskets  
- t65 loses revenue due to lower conversion  
- t50 balances both effects  

This is a classic free-shipping threshold tradeoff.

---

# 4. Guardrail Metrics

Guardrail metrics ensure that improvements in the primary metric do not harm the business.

---

## Free Shipping Qualification Rate

| Arm | Qualification Rate |
| --- | ------------------ |
| t35 | 71%                |
| t50 | 49%                |
| t65 | 33%                |

Interpretation:

Lower thresholds lead to more free shipping.

This increases subsidy exposure.

---

## Shipping Subsidy per Order

| Arm | Subsidy per Order |
| --- | ----------------- |
| t35 | 7.28              |
| t50 | 5.95              |
| t65 | 4.96              |

Interpretation:

Lower thresholds significantly increase shipping subsidy.

Higher thresholds reduce subsidy exposure.

---

## Negative Margin Orders

```
0% across all arms
```

This is acceptable for synthetic data.

In real ecommerce systems, this metric typically ranges between **1–5%**.

---

# 5. Decision Rule Application

The experiment decision rules state that a new threshold should be adopted only if:

1. Contribution margin per session improves  
2. Revenue per session is not materially harmed  
3. Guardrail metrics remain within acceptable ranges  

---

## Evaluation of t35

Contribution margin per session:

```
0.232 vs baseline 0.332
```

Result:

Significant decline.

Decision:

❌ Reject t35

---

## Evaluation of t65

Contribution margin per session:

```
0.334 vs baseline 0.332
```

Small improvement.

Revenue per session:

```
1.12 vs baseline 1.20
```

Revenue declines.

Guardrails:

- shipping subsidy improves  
- conversion declines  

---

# Final Decision

Recommended policy:

```
Maintain the current $50 free shipping threshold.
```

Reasoning:

- t35 materially reduces contribution margin  
- t65 provides only a negligible improvement in margin  
- t65 reduces revenue per session and conversion  
- t50 provides the best balance between conversion and basket size  

---

# Why This Is a Good Synthetic Experiment

This experiment produces a realistic outcome.

Many real-world experiments confirm that the **existing policy is already near optimal**.

Observed pattern:

| Arm | Outcome         |
| --- | --------------- |
| t35 | too generous    |
| t50 | balanced        |
| t65 | too restrictive |

This result demonstrates a common experiment outcome:

```
Current policy ≈ optimal policy
```

---

# Recommended Additional Analysis

Before producing the final experiment readout, two additional analyses should be performed.

## Confidence Intervals

Compute confidence intervals for:

- contribution margin per session  
- revenue per session  
- conversion rate  

This helps quantify uncertainty in the estimates.

---

## Treatment Effect Table

Example summary:

| Comparison | Δ CM per Session |
| ---------- | ---------------- |
| t35 vs t50 | -0.10            |
| t65 vs t50 | +0.002           |

This table makes the effect sizes easier to interpret.

---

# Final Assessment

The synthetic experiment generator produced:

- realistic behavioral tradeoffs  
- believable economic relationships  
- a non-obvious outcome  

This makes the experiment suitable for demonstrating a full experimentation workflow.