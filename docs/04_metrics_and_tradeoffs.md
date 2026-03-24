# Metrics & Tradeoffs

## Objective

Define metrics that reflect true business value and understand tradeoffs.

---

## Metric Types

### 1. North Star

- **Contribution Margin per Session**

Represents total business value per unit of traffic.

---

### 2. Input Metrics

- Conversion rate
- Average order value (AOV)
- Revenue per session

---

### 3. Guardrails

- Shipping subsidy per order
- Negative margin order rate
- Revenue per session

---

## Key Tradeoff

| Lower Threshold | Higher Threshold |
| --------------- | ---------------- |
| ↑ Conversion    | ↑ AOV            |
| ↑ Shipping cost | ↓ Conversion     |
| ↓ Profitability | ↓ Demand         |

---

## Observed Tradeoff

- $35:
  - High conversion
  - Low AOV
  - High subsidy → low margin

- $65:
  - Low conversion
  - High AOV
  - Lower subsidy → but reduced demand

- $50:
  - Balanced → highest revenue per session

---

## Key Insight

Optimizing conversion alone leads to poor profitability.

Optimizing AOV alone reduces demand.

The optimal policy balances both.

---

## Heuristic

Every improvement (conversion or AOV) comes with a cost.

Always identify what you are trading off.