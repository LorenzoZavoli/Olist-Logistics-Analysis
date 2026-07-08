----------------------------------- STUDY --------------------------------------------
-- Do delivery times/delays affect customer satisfaction?
-- In which geographical areas is the problem more pronounced, and how much revenue is at risk?
---------------------------------------------------------------------------------------

/*
Possible cases of interest:
1) ESTIMATED time greater than 7/14/21/more days
2) ACTUAL time greater than 7/14/21/more days
*/

----------------------------------- 1) DATA CLEANING -------------------------------------
/* 
 
create table shipping_time as 
select
ood.order_id,
ood.order_purchase_timestamp,
ood.order_approved_at,
ood.order_delivered_carrier_date,
ood.order_delivered_customer_date,
ood.order_estimated_delivery_date,
ocd.customer_state,
oord.review_score,
oord.review_comment_title,
oord.review_comment_message
from olist_orders_dataset ood
inner join olist_customers_dataset ocd on  ocd.customer_id = ood.customer_id
inner join olist_order_reviews_dataset oord on oord.order_id = ood.order_id
where ood.order_status = 'delivered';

select 
count(*) as total_rows,
count(distinct order_id) as distinct_orders
from shipping_time;
-- some orders have multiple reviews

select
  count(*) as total_delivered,
  count(*) filter (where order_purchase_timestamp in ('', '""')) as empty_purchase_date,
  count(*) filter (where order_delivered_customer_date in ('', '""')) as empty_delivered_date,
  count(*) filter (where order_estimated_delivery_date in ('', '""')) as empty_estimated_date  
  from olist_orders_dataset
where order_status = 'delivered';
-- 8 entries with empty "order_delivered_customer_date"
*/

drop table if exists order_delivery_time;

create table order_delivery_time as
with review_times as(
select
*,
row_number() over(partition by order_id order by review_creation_date desc) as review_number
from olist_order_reviews_dataset
) 
select
ood.order_id,
(ood.order_estimated_delivery_date::date - ood.order_purchase_timestamp::date) as expected_delivery_time,
(ood.order_delivered_customer_date::date - ood.order_purchase_timestamp::date) as delivery_time,
ocd.customer_state,
rt.review_score,
rt.review_comment_title,
rt.review_comment_message
from olist_orders_dataset ood
inner join olist_customers_dataset ocd on  ocd.customer_id = ood.customer_id
inner join review_times rt on rt.order_id = ood.order_id
where 
ood.order_status = 'delivered' and rt.review_number = 1
and ood.order_delivered_customer_date not in ('', '""')
and ood.order_estimated_delivery_date not in ('', '""')
and ood.order_purchase_timestamp not in ('', '""');

--------------------------------- 2) DATA AGGREGATION ------------------------------------
select
case 
	when delivery_time <=7 then '1. within 1 week delivery'
	when delivery_time <=14 then '2. within 2 weeks delivery'
	when delivery_time <=21 then '3. within 3 weeks delivery'
	when delivery_time <=28 then '4. within 4 weeks delivery'
	else '5. 4+ weeks delivery'
end as delivery_braket,
round(avg(review_score::numeric), 2) as avg_review_score,
count(*) as deliveries_number
from order_delivery_time 
group by delivery_braket 
order by delivery_braket  asc;

select
case 
	when (delivery_time - expected_delivery_time) <=0 then '1. no delay'
	when (delivery_time - expected_delivery_time) <=7 then '2. within 1 week delay'
	when (delivery_time - expected_delivery_time) <=14 then '3. within 2 weeks delay'
	when (delivery_time - expected_delivery_time) <=21 then '4. within 3 weeks delay'
	else '5. 3+ weeks delay'
end as delay_braket,
round(avg(review_score::numeric), 2) as avg_review_score,
count(*) as deliveries_number
from order_delivery_time 
group by delay_braket
order by delay_braket asc;

select
  round(corr(delivery_time::numeric, review_score::numeric)::numeric, 3) as corr_delivery_vs_score,
  round(corr((delivery_time - expected_delivery_time)::numeric, review_score::numeric)::numeric, 3) as corr_delay_vs_score
from order_delivery_time;

/*
with total_order_revenue as(
select 
order_id,
sum(price::numeric) as order_revenue	
from olist_order_items_dataset  
group by order_id
)
select 
odt.customer_state,
round(SUM(tor.order_revenue) filter (where odt.review_score::numeric <=2), 2) as unhappy_customers_revenue,
round(100.0 * sum(tor.order_revenue) filter (where odt.review_score::numeric <= 2) / sum(tor.order_revenue), 1) as pct_revenue_at_risk
from order_delivery_time odt
inner join total_order_revenue tor on tor.order_id = odt.order_id 
group by odt.customer_state
-- AP has no unhappy customers
*/

with total_order_revenue as(
select 
order_id,
sum(price::numeric) as order_revenue	
from olist_order_items_dataset  
group by order_id
)
select
odt.customer_state,
round(avg(odt.delivery_time), 0) as avg_delivery_days,
round(100.0 * count(*) filter (where odt.delivery_time > odt.expected_delivery_time) / count(*), 2) as pct_delay,
round(avg(odt.review_score::numeric), 2) as avg_review_score,
round(SUM(tor.order_revenue), 2) as total_state_revenue,
round(coalesce(SUM(tor.order_revenue) filter (where odt.review_score::numeric <=2), 0), 2) as unhappy_customers_revenue,
round(100.0 * coalesce(sum(tor.order_revenue) filter (where odt.review_score::numeric <= 2), 0) / sum(tor.order_revenue), 2) as pct_revenue_at_risk,
count(*) as deliveries_number
from order_delivery_time odt
inner join  total_order_revenue tor on tor.order_id = odt.order_id
group by odt.customer_state
order by total_state_revenue desc;

with total_order_revenue as(
select 
order_id,
sum(price::numeric) as order_revenue	
from olist_order_items_dataset  
group by order_id
)
select
'BRASIL (total)' as customer_state,
round(avg(odt.delivery_time), 0) as avg_delivery_days,
round(100.0 * count(*) filter (where odt.delivery_time > odt.expected_delivery_time) / count(*), 2) as pct_delay,
round(avg(odt.review_score::numeric), 2) as avg_review_score,
round(sum(tor.order_revenue), 2) as total_state_revenue,
round(coalesce(sum(tor.order_revenue) filter (where odt.review_score::numeric <= 2), 0), 2) as unhappy_customers_revenue,
round(100.0 * coalesce(sum(tor.order_revenue) filter (where odt.review_score::numeric <= 2), 0) / sum(tor.order_revenue), 2) as pct_revenue_at_risk,
count(*) as deliveries_number
from order_delivery_time odt
inner join total_order_revenue tor on tor.order_id = odt.order_id;





