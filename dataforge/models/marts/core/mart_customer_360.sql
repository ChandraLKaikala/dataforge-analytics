{{ config(
    materialized='table',
    contract={
        'enforced': true,
        'columns': [
            {'name': 'customer_id', 'data_type': 'integer', 'description': 'Unique customer ID'},
            {'name': 'first_name', 'data_type': 'varchar'},
            {'name': 'last_name', 'data_type': 'varchar'},
            {'name': 'country_code', 'data_type': 'varchar'},
            {'name': 'tier', 'data_type': 'varchar'},
            {'name': 'lifetime_value', 'data_type': 'decimal'},
            {'name': 'average_order_value', 'data_type': 'decimal'},
            {'name': 'total_orders', 'data_type': 'integer'},
            {'name': 'first_order_date', 'data_type': 'timestamp'},
            {'name': 'last_order_date', 'data_type': 'timestamp'},
            {'name': 'days_since_last_order', 'data_type': 'integer'},
            {'name': 'churn_risk_score', 'data_type': 'decimal'},
        ]
    }
) }}

with customer_base as (
  select
    c.customer_id,
    c.first_name,
    c.last_name,
    c.country_code,
    c.tier,
    c.created_at
  from {{ ref('stg_customers') }} c
),

order_metrics as (
  select
    co.customer_id,
    sum(o.total_amount) as lifetime_value,
    {{ safe_divide('sum(o.total_amount)', 'count(distinct o.order_id)', 0) }} as average_order_value,
    count(distinct o.order_id) as total_orders,
    min(o.order_date) as first_order_date,
    max(o.order_date) as last_order_date,
    datediff(day, max(o.order_date), current_date) as days_since_last_order
  from {{ ref('int_customer_orders') }} co
  join {{ ref('stg_orders') }} o on co.order_id = o.order_id
  where o.status = 'Completed'
  group by co.customer_id
),

churn_calculation as (
  select
    customer_id,
    lifetime_value,
    average_order_value,
    total_orders,
    first_order_date,
    last_order_date,
    days_since_last_order,
    case
      when days_since_last_order > 180 then 0.9
      when days_since_last_order > 90 then 0.6
      when days_since_last_order > 30 then 0.3
      else 0.0
    end as churn_risk_score
  from order_metrics
)

select
  cb.customer_id,
  cb.first_name,
  cb.last_name,
  cb.country_code,
  cb.tier,
  coalesce(cr.lifetime_value, 0) as lifetime_value,
  coalesce(cr.average_order_value, 0) as average_order_value,
  coalesce(cr.total_orders, 0) as total_orders,
  cr.first_order_date,
  cr.last_order_date,
  coalesce(cr.days_since_last_order, datediff(day, cb.created_at, current_date)) as days_since_last_order,
  coalesce(cr.churn_risk_score, 0.0) as churn_risk_score
from customer_base cb
left join churn_calculation cr on cb.customer_id = cr.customer_id
