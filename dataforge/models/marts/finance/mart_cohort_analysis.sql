{{ config(
    materialized='table',
    contract={
        'enforced': true,
        'columns': [
            {'name': 'cohort_month', 'data_type': 'date'},
            {'name': 'cohort_size', 'data_type': 'integer'},
            {'name': 'cohort_age_months', 'data_type': 'integer'},
            {'name': 'retained_customers', 'data_type': 'integer'},
            {'name': 'retention_rate', 'data_type': 'decimal'},
        ]
    }
) }}

with cohort_base as (
  select
    customer_id,
    trunc(first_order_date, 'month') as cohort_month
  from {{ ref('mart_customer_360') }}
  where first_order_date is not null
),

cohort_activity as (
  select
    cb.customer_id,
    cb.cohort_month,
    datediff(month, cb.cohort_month, cast(o.order_date as date)) as cohort_age_months
  from cohort_base cb
  join {{ ref('stg_orders') }} o on cb.customer_id = o.customer_id
  where o.status = 'Completed'
  group by cb.customer_id, cb.cohort_month, datediff(month, cb.cohort_month, cast(o.order_date as date))
),

cohort_summary as (
  select
    cohort_month,
    count(distinct customer_id) as cohort_size
  from cohort_base
  group by cohort_month
)

select
  ca.cohort_month,
  cs.cohort_size,
  ca.cohort_age_months,
  count(distinct ca.customer_id) as retained_customers,
  {{ safe_divide('count(distinct ca.customer_id)', 'cs.cohort_size', 0) }} as retention_rate
from cohort_activity ca
join cohort_summary cs on ca.cohort_month = cs.cohort_month
group by ca.cohort_month, cs.cohort_size, ca.cohort_age_months
order by ca.cohort_month desc, ca.cohort_age_months
