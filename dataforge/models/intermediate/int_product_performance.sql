{{ config(materialized='table') }}

with product_metrics as (
  select
    p.product_id,
    p.name,
    p.category,
    sum(oi.quantity) as total_units_sold,
    sum(oi.quantity * oi.unit_price) as total_revenue,
    sum(oi.quantity * (oi.unit_price - p.cost)) as gross_profit,
    avg(oi.unit_price) as avg_unit_price,
    count(distinct oi.order_id) as order_count
  from {{ ref('stg_products') }} p
  left join {{ ref('stg_order_items') }} oi on p.product_id = oi.product_id
  left join {{ ref('stg_orders') }} o on oi.order_id = o.order_id
  where o.status = 'Completed' or o.status is null
  group by p.product_id, p.name, p.category
)

select
  product_id,
  name,
  category,
  total_units_sold,
  total_revenue,
  gross_profit,
  avg_unit_price,
  order_count
from product_metrics
