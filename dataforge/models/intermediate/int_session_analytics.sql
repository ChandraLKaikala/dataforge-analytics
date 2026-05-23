{{ config(materialized='table') }}

with event_ordering as (
  select
    customer_id,
    event_id,
    event_date,
    event_type,
    session_duration_seconds,
    lag(event_date) over (partition by customer_id order by event_date) as prev_event_date,
    case
      when lag(event_date) over (partition by customer_id order by event_date) is null then 1
      when datediff(minute, lag(event_date) over (partition by customer_id order by event_date), event_date) > 30 then 1
      else 0
    end as is_new_session
  from {{ ref('stg_web_events') }}
),

session_grouping as (
  select
    customer_id,
    event_id,
    event_date,
    event_type,
    session_duration_seconds,
    sum(is_new_session) over (partition by customer_id order by event_date rows between unbounded preceding and current row) as session_number
  from event_ordering
),

sessions as (
  select
    md5(concat(customer_id, '_', session_number, '_', cast(min(event_date) as varchar))) as session_id,
    customer_id,
    min(event_date) as session_start,
    max(event_date) as session_end,
    count(*) as event_count,
    sum(session_duration_seconds) as total_session_duration_seconds,
    listagg(distinct event_type, ',') within group (order by event_type) as session_events
  from session_grouping
  group by customer_id, session_number
)

select
  session_id,
  customer_id,
  session_start,
  session_end,
  event_count,
  total_session_duration_seconds,
  session_events
from sessions
