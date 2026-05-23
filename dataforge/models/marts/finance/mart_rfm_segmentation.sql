{{ config(
    materialized='table',
    contract={
        'enforced': true,
        'columns': [
            {'name': 'customer_id', 'data_type': 'integer'},
            {'name': 'recency_days', 'data_type': 'integer'},
            {'name': 'frequency', 'data_type': 'integer'},
            {'name': 'monetary', 'data_type': 'decimal'},
            {'name': 'r_score', 'data_type': 'integer'},
            {'name': 'f_score', 'data_type': 'integer'},
            {'name': 'm_score', 'data_type': 'integer'},
            {'name': 'rfm_segment', 'data_type': 'varchar'},
        ]
    }
) }}

with rfm_calc as (
  select
    customer_id,
    datediff(day, max(last_order_date), current_date) as recency_days,
    total_orders as frequency,
    lifetime_value as monetary
  from {{ ref('mart_customer_360') }}
  where lifetime_value > 0
),

rfm_scoring as (
  select
    customer_id,
    recency_days,
    frequency,
    monetary,
    ntile(5) over (order by recency_days desc) as r_score,
    ntile(5) over (order by frequency asc) as f_score,
    ntile(5) over (order by monetary asc) as m_score
  from rfm_calc
),

segment_mapping as (
  select
    customer_id,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    case
      when r_score >= 4 and f_score >= 4 and m_score >= 4 then 'Champions'
      when r_score >= 3 and f_score >= 3 and m_score >= 3 then 'Loyal Customers'
      when r_score >= 3 and f_score <= 2 and m_score >= 3 then 'Potential Loyalists'
      when r_score <= 2 and f_score >= 4 and m_score >= 4 then 'At Risk'
      when r_score <= 2 and f_score <= 2 and m_score <= 2 then 'Lost'
      else 'Needs Attention'
    end as rfm_segment
  from rfm_scoring
)

select
  customer_id,
  recency_days,
  frequency,
  monetary,
  r_score,
  f_score,
  m_score,
  rfm_segment
from segment_mapping
order by rfm_segment, monetary desc
