{{ config(materialized='table') }}

with customer_orders as (
  select
    o.customer_id,
    o.order_id,
    o.order_date,
    o.total_amount,
    row_number() over (partition by o.customer_id order by o.order_date) as order_number,
    count(*) over (partition by o.customer_id order by o.order_date rows between unbounded preceding and current row) as order_count_to_date,
    sum(o.total_amount) over (partition by o.customer_id order by o.order_date rows between unbounded preceding and current row) as cumulative_revenue_to_date,
    first_value(o.order_date) over (partition by o.customer_id order by o.order_date) as first_order_date,
    datediff(day, lag(o.order_date) over (partition by o.customer_id order by o.order_date), o.order_date) as days_since_last_order
  from {{ ref('stg_orders') }} o
  where o.status = 'Completed'
)

select
  customer_id,
  order_id,
  order_count_to_date,
  cumulative_revenue_to_date,
  first_order_date,
  days_since_last_order
from customer_orders
