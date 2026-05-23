{{ config(materialized='view') }}

select
  cast(campaign_id as integer) as campaign_id,
  cast(name as varchar) as name,
  cast(channel as varchar) as channel,
  cast(budget as decimal(10,2)) as budget,
  cast(start_date as date) as start_date,
  cast(end_date as date) as end_date,
  current_timestamp as _loaded_at
from {{ source('raw_ecommerce', 'campaigns') }}
where campaign_id is not null
  and name is not null
