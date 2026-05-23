-- Test: Ensure revenue from mart_revenue_analytics matches source order totals
select
  count(*) as discrepancy_count
from (
  select
    sum(total_revenue) as mart_revenue
  from {{ ref('mart_revenue_analytics') }}
) mart
join (
  select
    sum(total_amount) as source_revenue
  from {{ ref('stg_orders') }}
  where status = 'Completed'
) src
where abs(mart.mart_revenue - src.source_revenue) > 0.01
having count(*) > 0
