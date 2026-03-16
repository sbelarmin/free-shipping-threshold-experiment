### _End-to-end experimentation framework demonstrating experiment design, metric development, power analysis, diagnostics, and decision analysis for an ecommerce free-shipping policy test._

---

# Free Shipping Threshold Experiment

## Project Snapshot

| Item                  | Summary                                        |
| --------------------- | ---------------------------------------------- |
| Business Problem      | Determine optimal free-shipping threshold      |
| Experiment Type       | A/B/n experiment                               |
| Treatments            | $35, $50 (control), $65                        |
| Unit of Randomization | Session                                        |
| Primary Metric        | Contribution Margin per Session                |
| Diagnostics           | SRM test, traffic balance checks               |
| Key Finding           | $50 threshold maximizes profitability          |
| Tools Used            | Python, Pandas, SciPy, Statsmodels, Matplotlib |

---

# Business Question

What free-shipping threshold maximizes **contribution margin per session** while maintaining strong customer conversion?

E-commerce teams frequently adjust free-shipping thresholds to balance customer demand and shipping costs. Lower thresholds may increase conversion but reduce profitability due to higher shipping subsidies, while higher thresholds can increase average order value but reduce overall demand.

This project simulates and analyzes an A/B experiment to determine the optimal threshold.

---

# Executive Summary

### Experiment Setup

Customers were randomly assigned to one of three free-shipping thresholds:

| Treatment | Threshold                       |
| --------- | ------------------------------- |
| T35       | Free shipping at $35            |
| T50       | Free shipping at $50 (baseline) |
| T65       | Free shipping at $65            |

### Primary Metric

Contribution Margin per Session (CM / Session)

### Key Results

| Treatment | Conversion Rate | Avg Order Value | CM per Session |
| --------- | --------------- | --------------- | -------------- |
| T35       | 2.21%           | $44             | $0.232         |
| T50       | 2.05%           | $55             | $0.332         |
| T65       | 1.75%           | $60             | $0.334         |


### Recommendation

Maintain the **$50 free-shipping threshold**.

While the $35 threshold increases conversion, shipping subsidies reduce overall profitability.  
The $65 threshold increases order value but reduces demand too much to compensate.

The $50 threshold provides the best balance of conversion and profitability.

---

# Key Plots

Below is the comparison of contribution margin per session across treatments.

![Contribution Margin Comparison](reports/figures/cm_per_session_comparison.png)

---  

Below is the conversion and average order value tradeoff across treatments.  

![Conversion AOV Tradeoff](reports/figures/conversion_tradeoff.png)

# Experiment Design

### Unit of Randomization

Session-level randomization

### Treatments

Three thresholds tested:

- $35 free shipping
- $50 free shipping (control)
- $65 free shipping

### Hypotheses

Lower Threshold ($35)

- Conversion increases
- Average order value decreases
- Shipping subsidies increase
- Contribution margin may decline

Higher Threshold ($65)

- Conversion decreases
- Average order value increases
- Shipping subsidies decrease
- Net profitability uncertain

---

# Metrics

### Primary Metric

Contribution Margin per Session

Contribution Margin = Revenue − Product Cost − Shipping Cost

Why this metric?

Shipping promotions directly affect profitability. Measuring margin per session captures both demand changes and cost implications.

---

### Secondary Metrics

| Metric              | Purpose              |
| ------------------- | -------------------- |
| Conversion Rate     | Demand sensitivity   |
| Average Order Value | Basket size changes  |
| Revenue per Session | Top-line performance |
| Orders              | Volume impact        |

---

### Guardrail Metrics  

| Metric                     | Purpose                                                    |
| -------------------------- | ---------------------------------------------------------- |
| Shipping Subsidy per Order | Ensure shipping incentives are financially sustainable     |
| Negative Margin Order Rate | Ensure we are not creating significant unprofitable orders |
| Revenue per Session        | Ensure we are not sacrificing revenue for margin           |

---

# Business Decision Rules  

A new free-shipping threshold will be recommended only if it: 

    1. Imporves contribution margin per session relative to the current $50 threshold by a statistically significant and economically meaningful amount.  
    2. Does not materially reduce revenue per session and conversion rate.  
    3. Does not create unacceptable movement in guardrail metrics  

The experiment design and results should be reviewed before rollout if:   

    1. Contribution margin per session improves, but revenue or guardrails worsen by a meaningful amount  

The free-shipping rollout should remain in place at $50 if:   

    1. Contribution margin per session does not improve  

---  

# Data Generation

This project uses **synthetic data** to simulate realistic e-commerce customer behavior.

Simulated features include:

- sessions
- conversion behavior
- order value
- shipping eligibility
- shipping cost
- product margin

Synthetic data allows the experiment analysis to be reproduced without using proprietary data.

---  

# Power Analysis  

A power analysis was performed to ensure the experiment has a good chance of detecting meaningful improvement in contribution margin per session (primary metric) by providing: 

        1. How much data do we need?
        2. How long should we run the experiment?  

Results:   

| Parameter                           | Value     |
| ----------------------------------- | --------- |
| Avg. Session per Day                | 10,000    |
| Minimum Detectible Effect           | 0.025     |
| Experiment Arms                     | 3         |
| Alpha                               | 0.05      |
| Power                               | 0.80      |
| Sample size per arm                 | ~ 150,000 |
| Test duration                       | ~ 45 days |
| Minimum Est. Annual Business Impact | ~ $91,000 |

---

# Diagnostics

Before estimating treatment effects, standard experiment diagnostics were performed.

### Sample Ratio Mismatch (SRM)

Chi-square test confirmed balanced traffic allocation.

| Check           | Result       |
| --------------- | ------------ |
| SRM             | Not detected |
| Traffic Balance | Passed       |

### Data Quality

Basic validation checks:

- no duplicate sessions
- non-negative revenue
- reasonable order values

---

# Analysis Methods

Treatment effects were evaluated using:

- mean comparison
- t-tests
- confidence intervals
- lift calculations

The analysis focuses on **practical business impact**, not just statistical significance.

---

# Future Improvements

Possible extensions:

- heterogeneous treatment effects by customer segment
- shipping elasticity modeling
- longer-term retention impact
- Bayesian experiment analysis

---

# Author

Scott Belarmino  
Data Science Portfolio Project  
## Note on Tooling

Large language models (LLMs) were used to assist with documentation organization and readability improvements in this project.  

All experiment design, data generation logic, analysis methodology, and interpretation were developed and verified by the author.