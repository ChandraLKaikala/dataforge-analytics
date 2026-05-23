{{ config(
    materialized='table',
    contract={
        'enforced': true,
        'columns': [
            {'name': 'event_type', 'data_type': 'varchar'},
            {'name': 'unique_customers', 'data_type': 'integer'},
            {'name': 'event_count', 'data_type': 'integer'},
            {'name': 'conversion_rate_to_purchase', 'data_type': 'decimal'},
            {'name': 'revenue_from_funnel_step', 'data_type': 'decimal'},
        ]
    }
) }}

with event_funnel as (
  select
    event_type,
    count(distinct customer_id) as unique_customers,
    count(*) as event_count
  from {{ ref('stg_web_events') }}
  group by event_type
),

event_to_order as (
  select
    we.event_type,
    count(distinct we.customer_id) as customers_with_orders,
    sum(o.total_amount) as revenue_from_funnel_step
  from {{ ref('stg_web_events') }} we
  join {{ ref('stg_orders') }} o on we.customer_id = o.customer_id and we.event_date < o.order_date
  where o.status = 'Completed'
  group by we.event_type
)

select
  ef.event_type,
  ef.unique_customers,
  ef.event_count,
  {{ safe_divide('efo.customers_with_orders', 'ef.unique_customers', 0) }} as conversion_rate_to_purchase,
  coalesce(efo.revenue_from_funnel_step, 0) as revenue_from_funnel_step
from event_funnel ef
left join event_to_order efo on ef.event_type = efo.event_type
