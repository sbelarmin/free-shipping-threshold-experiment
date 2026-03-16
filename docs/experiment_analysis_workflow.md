# Experiment Analysis Workflow — Free Shipping Threshold Experiment

Before analyzing experiment results, it is important to follow a structured workflow.  
Teams at companies like **Google, Airbnb, Netflix, and Meta** typically follow a disciplined sequence when reviewing experiments so that conclusions are not drawn prematurely from topline metrics.

This section outlines the full analysis workflow that will be used in the experiment notebook.

---

# Experiment Analysis Workflow

## Step 1 — Confirm the Experiment is Trustworthy

Before interpreting any results, verify that the experiment ran correctly and that the data can be trusted.

This includes:

- Sample Ratio Mismatch (SRM) check
- Visitor assignment consistency
- Metric formula validation
- Basic data sanity checks

If any of these checks fail, the experiment results should not be interpreted until the issue is resolved.

---

## Step 2 — Reconfirm the Metric Framework

Restate the metric framework before analysis so the evaluation remains anchored to the predefined success criteria.

This includes defining:

- Primary metric
- Secondary metrics
- Guardrail metrics
- Exact formulas used to calculate each metric

This step ensures that the analysis stays aligned with the original experiment design.

---

## Step 3 — Build Topline Experiment Summaries

Construct the arm-level summary table for the test period.

Typical metrics in this table include:

- Sessions
- Orders
- Conversion rate
- Average Order Value (AOV)
- Revenue per session
- Contribution margin per session
- Free shipping qualification rate
- Shipping subsidy metrics

This table provides the first overview of experiment performance.

---

## Step 4 — Evaluate the Primary Metric

Focus first on the primary decision metric.

For this experiment, the primary metric is:

Contribution Margin per Session

The analysis should include:

- Comparing CM per session across arms
- Computing absolute lift vs baseline
- Computing relative lift vs baseline
- Identifying the potential winning variant

The primary metric determines the main economic impact of the experiment.

---

## Step 5 — Evaluate Secondary Metrics

Secondary metrics help explain **why** the primary metric behaved the way it did.

For the free shipping threshold experiment, these include:

- Conversion rate
- Average Order Value (AOV)
- Revenue per session
- Free shipping qualification rate

These metrics reveal the behavioral mechanism behind the experiment outcome.

---

## Step 6 — Evaluate Guardrail Metrics

Guardrail metrics ensure that improvements in the primary metric do not cause unacceptable harm to the business.

Typical guardrail checks include:

- Shipping subsidy per order
- Negative margin order rate
- Revenue impact

Guardrails help ensure the experiment remains economically sustainable.

---

## Step 7 — Estimate Uncertainty

Once topline metrics are evaluated, the next step is to quantify uncertainty.

This includes:

- Confidence intervals
- Hypothesis testing
- Treatment effect estimation
- Practical significance review

Observed differences should be evaluated to determine whether they are statistically reliable and economically meaningful.

---

## Step 8 — Interpret the Business Tradeoff

Translate the metric changes into a clear behavioral and economic story.

This step explains:

- Why one threshold performed better or worse
- The tradeoff between conversion and basket size
- The impact of shipping economics
- Customer behavior under different thresholds

This interpretation connects the statistical results to real business dynamics.

---

## Step 9 — Apply the Decision Rule

Use the predefined business decision rules to determine the experiment outcome.

This includes deciding whether to:

- Roll out a new threshold
- Keep the existing policy
- Run additional experiments

The decision should be consistent with the experiment design established before the test began.

---

## Step 10 — Write the Experiment Readout

The final step is preparing the experiment readout that would be shared with stakeholders.

A typical experiment readout includes:

- Objective
- Experiment design
- Metrics
- Results
- Decision
- Recommended next steps

This step translates the analysis into a clear narrative for product, engineering, and leadership teams.

---

# Recommended Notebook Structure

The experiment analysis notebook (`02_experiment_analysis.ipynb`) will follow this structure:

1. Load experiment data and define analysis scope  
2. Run experiment diagnostics  
3. Restate metric framework  
4. Build topline experiment summary table  
5. Analyze the primary metric  
6. Analyze secondary metrics  
7. Analyze guardrail metrics  
8. Estimate uncertainty  
9. Apply decision rule  
10. Draft final recommendation

---

# Recommended Starting Point

The analysis should begin with:

**Step 1 — Load the experiment data and run diagnostics.**

This is the correct starting point because if the experiment data is not trustworthy, all downstream analysis becomes unreliable.