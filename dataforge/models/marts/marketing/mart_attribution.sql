{{ config(
    materialized='table',
    contract={
        'enforced': true,
        'columns': [
            {'name': 'campaign_id', 'data_type': 'integer'},
            {'name': 'campaign_name', 'data_type': 'varchar'},
            {'name': 'channel', 'data_type': 'varchar'},
            {'name': 'first_touch_revenue', 'data_type': 'decimal'},
            {'name': 'last_touch_revenue', 'data_type': 'decimal'},
            {'name': 'linear_touch_revenue', 'data_type': 'decimal'},
            {'name': 'attributed_conversions', 'data_type': 'integer'},
            {'name': 'avg_days_to_conversion', 'data_type': 'decimal'},
        ]
    }
) }}

with campaign_data as (
  select
    c.campaign_id,
    c.name,
    c.channel,
    sum(ca.first_touch_revenue) as first_touch_revenue,
    sum(ca.last_touch_revenue) as last_touch_revenue,
    sum(ca.linear_touch_revenue) as linear_touch_revenue,
    count(distinct ca.order_id) as attributed_conversions,
    avg(ca.days_to_conversion) as avg_days_to_conversion
  from {{ ref('stg_campaigns') }} c
  left join {{ ref('int_campaign_attribution') }} ca on c.campaign_id = ca.campaign_id
  group by c.campaign_id, c.name, c.channel
)

select
  campaign_id,
  name as campaign_name,
  channel,
  coalesce(first_touch_revenue, 0) as first_touch_revenue,
  coalesce(last_touch_revenue, 0) as last_touch_revenue,
  coalesce(linear_touch_revenue, 0) as linear_touch_revenue,
  attributed_conversions,
  avg_days_to_conversion
from campaign_data
