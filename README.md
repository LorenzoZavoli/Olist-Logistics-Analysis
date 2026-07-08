# Does Delivery Time Hurt Customer Satisfaction? — Olist E-Commerce Analysis

SQL analysis from the Brazilian e-commerce platform Olist, answering three questions:
1. Do delivery times and delays affect customer satisfaction?
2. Which geographic regions are hit hardest?
3. How much revenue is currently at risk because of it?

> **Yes**, both delivery time and delay are linked to satisfaction (correlation of **-0.33** and **-0.27**, respectively). Nationally, **15.1% of revenue (R$1.23M)** comes from orders rated ≤2 stars. The risk isn't evenly spread: **Rio de Janeiro**, Brazil's 2nd largest market by revenue, runs at **20.3%** revenue-at-risk, a third above the national average, while the largest market, São Paulo, is below it at 12.3%.

---

## 1. Dataset & Tools

- **Data:** [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (orders, customers, order items, reviews), filtered to `order_status = 'delivered'`.
- **Tools:** PostgreSQL for data cleaning/aggregation, Python (pandas + matplotlib) for visualization.
- **Scope:** Orders with a valid purchase date, estimated delivery date, and actual delivered date (8 orders with missing delivery dates were excluded). Orders with multiple reviews keep only the most recent one, to avoid double-counting. 

---

## 2. Does delivery time affect satisfaction?

Grouping orders by how long delivery actually took, the average review score falls from **4.41** (delivered within a week) to **2.33** (delivered in 4+ weeks).

![Customer satisfaction vs Delivery time](images/01_score_delivery.png)


However, it is necessary to take into account also the delay of an order. In fact, a 3+ week delivery could be fine if it was quoted upfront. This is where the impact is most significant: orders delivered on time or early average **4.29**, but as soon as an order is delayed at all, the score collapses to **2.67**, and keeps falling toward **~1.6-1.8** for longer delays. Missing the promised date, even briefly, matters more to customers than absolute delivery speed.

![Customer satisfaction vs Delay](images/02_score_delay.png)

Pearson correlation analysis confirms that both delivery time and delay negatively impact the review score (**-0.33** and **-0.27**, respectively).

---

## 3. Where is the problem worse?

The plot of % of delayed deliveries against average review score varies significantly by state. Here, the color intensity of each dot represents the % of revenue at risk. To ensure the focus remains on the areas with the highest business impact, the states that generate less than 0.5% of Brazil's total revenue are displayed with reduced opacity.

![Percentage of delays vs Average review score, per state](images/04_scatter.png)

States to the right (more delays) consistently sit lower (worse scores). **SE, MA, PA, CE** and **RJ** stand out as critical areas, combining above-average delay rates with below-average satisfaction.

---

## 4. How much revenue is at risk?

Nationally, **15.1%** of Olist's revenue (R$1.23M out of R$8.15M) comes from orders with a review score of 2 stars or lower. While the percentage of revenue at risk varies significantly across states, it is crucial to interpret these figures through the lens of market scale.

![Percentage of revenue at risk by state](images/03_revenue_risk_state.png)

Some states, such as SE or RR, exhibit high percentages of revenue at risk; however, these figures are driven by extremely low order volumes, resulting in a negligible impact on the company's total financial performance. 

Instead, Rio de Janeiro (RJ) is the second-largest market by revenue and faces a 20.3% risk, representing a critical area. By contrast, **SP** (São Paulo), the single largest market at 38.6% of national revenue, actually performs *better* than the national average (12.3% revenue at risk).


*Data source: [Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle, CC BY-NC-SA 4.0).*