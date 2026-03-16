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

_Please see the end of this document for experiment replication instructions._ 


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

# Experiment Results  

The experiment was designed to evaluate which free shipping threshold maximizes contribution margin while maintaining healthy customer behavior and sustainable shipping economics.

The predefined decision framework was:  
        1. The **primary metric (Contribution Margin per Session)** determines the winning treatment.  
        2. **Secondary metrics** explain the behavioral mechanism  
        3. **Guardrail metrics** ensure the policy does not harm the business  
        4. **Uncertainty analysis** ensures the observed effects are reliable  

---

## 1. Primary Metric Result

Contribution margin per session:

| Arm | CM per Session |
| --- | -------------- |
| t35 | 0.232          |
| t50 | 0.332          |
| t65 | 0.334          |

Observations:

    - `t35` performs substantially worse than the baseline.
    - `t50` and `t65` perform nearly identically.
    - `t65` is slightly higher than `t50`, but the improvement is extremely small.

The observed difference between `t65` and `t50` is:

```
+0.002 CM per session
```

This represents a relative lift of approximately:

```
~0.6%
```

---

## 2. Secondary Metric Interpretation

Secondary metrics explain the behavioral mechanism behind the results.

| Arm | Conversion | AOV      | Revenue / Session |
| --- | ---------- | -------- | ----------------- |
| t35 | highest    | lowest   | lowest            |
| t50 | moderate   | moderate | highest           |
| t65 | lowest     | highest  | moderate          |

Interpretation:

    - Lower thresholds increase conversion but reduce basket size.
    - Higher thresholds reduce conversion but increase basket size.
    - The $50 threshold produces the best balance of conversion and order value.

---

## 3. Guardrail Metrics

Guardrail metrics ensure the experiment does not introduce unacceptable risk.

| Arm | Shipping Subsidy | Negative Margin Orders |
| --- | ---------------- | ---------------------- |
| t35 | highest          | 0%                     |
| t50 | moderate         | 0%                     |
| t65 | lowest           | 0%                     |

Interpretation:

    - Lower thresholds increase shipping subsidy exposure.
    - Higher thresholds reduce shipping costs but at the expense of conversion.
    - No treatment created negative margin orders.

---

## 4. Uncertainty Analysis

Confidence intervals and hypothesis tests indicate:

    - `t35` performs **significantly worse** than the baseline.
    - The difference between `t65` and `t50` is **not statistically significant**.

The confidence intervals for `t50` and `t65` overlap substantially.

This indicates that the observed difference between the two arms is likely due to random variation.  

| Threshold vs. Baseline   | Value       |
| ------------------------ | ----------- |
| t-stat for t65 vs. t50:  | 0.2288      |
| p_value for t65 vs. t50: | 0.81896     |
| t-stat for t35 vs. t50:  | -13.3216    |
| p_value for t35 vs. t50: | 1.77882e-51 |

---

# Final Decision

Based on the experiment results, the recommended policy is:

```
Maintain the current $50 free shipping threshold.
```

Reasoning:

    1. The $35 threshold significantly harms profitability.
    2. The $65 threshold provides only a negligible improvement in margin.
    3. The $65 threshold reduces revenue per session and conversion.
    4. The difference between $50 and $65 is not statistically significant.

Therefore, there is insufficient evidence that changing the threshold would improve business outcomes.

---

# Key Takeaway

The experiment suggests that the current $50 threshold is already close to optimal.

The experiment does provide valuable insight by validating the current pricing and shipping strategy.  

---
# Future Improvements

Possible extensions:

- heterogeneous treatment effects by customer segment
- shipping elasticity modeling
- longer-term retention impact
- Bayesian experiment analysis

---

# Author

## Scott Belarmino  
Data Science Portfolio Project  

---  
### Note on Tooling

Large language models (LLMs) were used to assist with documentation organization and readability improvements in this project.  
All experiment design, data generation logic, analysis methodology, and interpretation were developed and verified by the author.  

---  

## Reproducing the Synthetic Experiment

This project includes a configuration-driven synthetic data generator so the entire experiment can be reproduced end-to-end.

The steps below allow a viewer to regenerate the synthetic dataset and rerun the analysis notebook.

---

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd project_2_ab_testing
```

---

### 2. Create and Activate a Virtual Environment

#### Mac / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If a `requirements.txt` file is not available yet, install the core packages manually:

```bash
pip install pandas numpy scipy statsmodels pyyaml matplotlib jupyter nbconvert
```

---

### 4. Review the Experiment Configuration

The synthetic data assumptions are stored in:

```
configs/experiment_config.yaml
```

This configuration file controls the simulated business environment, including:

- experiment arms
- conversion rates
- target average order values
- free shipping qualification rates
- shipping cost assumptions
- traffic assumptions
- experiment dates
- basket generation parameters

You can modify this file to simulate different business scenarios.

---

### 5. Generate the Synthetic Dataset

Run the synthetic data pipeline from the project root directory:

```bash
python src/simulation/generate_free_shipping_experiment.py
```

This script generates session-level synthetic data representing user visits, orders, and associated economics.

The dataset will be saved to:

```
data/synthetic/free_shipping_experiment_sessions.csv
```

---

### 6. Run the Experiment Analysis Notebook

Launch Jupyter:

```bash
jupyter notebook
```

Open the analysis notebook:

```
notebooks/02_experiment_analysis.ipynb
```

Run all cells to reproduce the experiment workflow, including:

- experiment diagnostics
- sample ratio mismatch checks
- experiment summary tables
- primary metric analysis
- behavioral mechanism analysis
- guardrail metric validation
- statistical inference
- confidence interval estimation
- experiment decision analysis

---

### 7. Optional: Regenerate Data with a Different Random Seed

The synthetic generator uses a fixed random seed for reproducibility.

To generate a different dataset, update the seed in:

```
src/simulation/generate_free_shipping_experiment.py
```

Example:

```python
if __name__ == "__main__":
    main(seed=42)
```

Change the seed value (for example to `123`) and rerun the generator.

---

### 8. Optional: Export the Analysis Notebook

To export the notebook to HTML:

```bash
jupyter nbconvert --to html notebooks/02_experiment_analysis.ipynb
```

The HTML file can then be opened in a browser and printed to PDF if desired.

---

### Expected Outputs

After running the pipeline, viewers should be able to reproduce:

- the synthetic session-level experiment dataset
- summary metrics for each free shipping threshold
- statistical comparisons between experiment arms
- the final business recommendation

For reproducibility, all experiment assumptions are centralized in:

```
configs/experiment_config.yaml
```

and synthetic data generation is deterministic when using a fixed random seed.