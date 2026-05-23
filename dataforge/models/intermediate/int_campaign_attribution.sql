{{ config(materialized='table') }}

with campaign_touches as (
  select
    we.campaign_id,
    we.customer_id,
    o.order_id,
    we.event_date,
    o.order_date,
    o.total_amount,
    row_number() over (partition by we.customer_id, o.order_id order by we.event_date) as first_touch,
    row_number() over (partition by we.customer_id, o.order_id order by we.event_date desc) as last_touch,
    count(*) over (partition by we.customer_id, o.order_id) as total_touches
  from {{ ref('stg_web_events') }} we
  join {{ ref('stg_orders') }} o on we.customer_id = o.customer_id and we.event_date < o.order_date
  where we.campaign_id is not null and o.status = 'Completed'
),

attribution as (
  select
    campaign_id,
    customer_id,
    order_id,
    total_amount,
    case when first_touch = 1 then total_amount else 0 end as first_touch_revenue,
    case when last_touch = 1 then total_amount else 0 end as last_touch_revenue,
    (total_amount / total_touches) as linear_touch_revenue,
    datediff(day, event_date, order_date) as days_to_conversion
  from campaign_touches
)

select
  campaign_id,
  customer_id,
  order_id,
  max(first_touch_revenue) as first_touch_revenue,
  max(last_touch_revenue) as last_touch_revenue,
  sum(linear_touch_revenue) as linear_touch_revenue,
  min(days_to_conversion) as days_to_conversion
from attribution
group by campaign_id, customer_id, order_id
