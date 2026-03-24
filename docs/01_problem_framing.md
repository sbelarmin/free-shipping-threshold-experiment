# Problem Framing

## Objective

Determine the optimal free shipping threshold that maximizes contribution margin while maintaining healthy customer behavior.

---

## Step 1: Separate Business vs Causal Question

**Business Question:**
> What free-shipping threshold should we use to maximize profitability?

**Causal Question:**
> What is the causal impact of changing the free shipping threshold on contribution margin per session?

---

## Step 2: Identify the System

Key drivers of the system:

- Free shipping threshold
- Conversion rate
- Average order value (AOV)
- Shipping cost / subsidy
- Customer purchase behavior

Key relationships:

- Lower threshold → higher conversion, lower AOV, higher shipping cost  
- Higher threshold → lower conversion, higher AOV, lower shipping cost  

---

## Step 3: Define the Unit of Analysis

- **Unit of Randomization:** Session  
- **Unit of Analysis:** Session  

Each session represents a customer visit with a potential purchase outcome.

---

## Step 4: Define Success Metric

Primary metric:

- **Contribution Margin per Session**

Why:

- Captures both demand (conversion) and economics (costs)
- Aligns directly with business profitability

---

## Step 5: Identify Threats to Validity

- Selection bias (e.g., high-value users behave differently)
- Seasonality (e.g., holidays affecting demand)
- Simultaneous promotions
- Measurement errors in revenue or cost

---

## Heuristic

If we cannot clearly state:
> “Which threshold increases contribution margin per session?”

then the problem is not well defined.