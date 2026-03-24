# Common Mistakes

## 1. Confusing Correlation with Causation

Without randomization, higher AOV customers might appear to benefit from higher thresholds.

This would incorrectly attribute performance to the threshold.

---

## 2. Ignoring Selection Bias

High-value users may naturally reach free shipping thresholds.

Randomization is required to remove this bias.

---

## 3. Over-focusing on Point Estimates

Example:

- $65 CM/session = 0.334
- $50 CM/session = 0.332

Naively choosing $65 ignores:

- confidence intervals
- statistical significance

---

## 4. Misinterpreting Confidence Intervals

95% CI does not mean:

> “95% chance the true value is in the interval”

Correct interpretation:

- If we repeated the experiment many times, 95% of intervals would contain the true value

---

## 5. Ignoring Guardrail Metrics

A treatment may improve margin but harm:

- revenue
- customer experience

Example:

- $65 reduces conversion and revenue per session

---

## 6. Optimizing the Wrong Metric

Focusing on:

- conversion → leads to $35 (bad)
- AOV → leads to $65 (not ideal)

Correct metric:

- **Contribution margin per session**

---

## Final Thought

The hardest part is not analysis — it is making the correct decision under uncertainty.

In this experiment:

- $65 is slightly higher
- but not meaningful

Correct decision:

> Keep the $50 threshold