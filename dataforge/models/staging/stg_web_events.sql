{{ config(materialized='view') }}

select
  cast(event_id as integer) as event_id,
  cast(customer_id as integer) as customer_id,
  cast(event_type as varchar) as event_type,
  cast(nullif(product_id, 0) as integer) as product_id,
  cast(nullif(campaign_id, 0) as integer) as campaign_id,
  cast(event_date as timestamp) as event_date,
  cast(session_duration_seconds as integer) as session_duration_seconds,
  current_timestamp as _loaded_at
from {{ source('raw_ecommerce', 'web_events') }}
where event_id is not null
  and customer_id is not null
  and event_date is not null
