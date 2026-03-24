# Causal Inference

## Objective

Estimate causal effects when randomization is not possible.

---

## The Core Problem

Correlation ≠ Causation

Example:
- Lowest price sellers win Buy Box more often
- But they also:
  - Use FBA
  - Have better ratings

 Confounding bias

---

## Methods

### 1. Matching / Propensity Scores

Goal:
- Compare similar units

Use when:
- You can model treatment probability

---

### 2. Regression Adjustment

Control for:
- Observed confounders

Limitation:
- Only works for observed variables

---

### 3. Difference-in-Differences (DiD)

Use when:
- You have before/after + control group

---

## Key Insight

Naive estimates often overstate impact

---

## Common Failure Modes

- Ignoring unobserved confounding
- Treating adjusted results as “truth”
- Not validating assumptions

---

##  Heuristic

Ask:
> “What would have happened if this unit did NOT receive treatment?”

If you can’t answer that, you don’t have causality.