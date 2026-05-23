{{ config(
    materialized='table',
    contract={
        'enforced': true,
        'columns': [
            {'name': 'revenue_date', 'data_type': 'date'},
            {'name': 'total_revenue', 'data_type': 'decimal'},
            {'name': 'total_orders', 'data_type': 'integer'},
            {'name': 'average_order_value', 'data_type': 'decimal'},
            {'name': 'total_units_sold', 'data_type': 'integer'},
            {'name': 'total_discounts', 'data_type': 'decimal'},
            {'name': 'gross_profit', 'data_type': 'decimal'},
            {'name': 'profit_margin', 'data_type': 'decimal'},
        ]
    }
) }}

with daily_revenue as (
  select
    cast(o.order_date as date) as revenue_date,
    sum(o.total_amount) as total_revenue,
    count(distinct o.order_id) as total_orders,
    {{ safe_divide('sum(o.total_amount)', 'count(distinct o.order_id)', 0) }} as average_order_value,
    sum(oi.quantity) as total_units_sold,
    sum(oi.discount_amount) as total_discounts,
    sum(oi.quantity * (oi.unit_price - p.cost)) as gross_profit
  from {{ ref('stg_orders') }} o
  join {{ ref('stg_order_items') }} oi on o.order_id = oi.order_id
  join {{ ref('stg_products') }} p on oi.product_id = p.product_id
  where o.status = 'Completed'
  group by cast(o.order_date as date)
)

select
  revenue_date,
  total_revenue,
  total_orders,
  average_order_value,
  total_units_sold,
  total_discounts,
  gross_profit,
  {{ safe_divide('gross_profit', 'total_revenue', 0) }} as profit_margin
from daily_revenue
order by revenue_date desc
