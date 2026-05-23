{{ config(
    materialized='view',
    tags=['pii']
) }}

select
  customer_id,
  md5(coalesce(email, 'unknown')) as email_hash,
  first_name,
  last_name,
  country,
  tier,
  created_at,
  now() as _loaded_at
from raw.customers
where customer_id is not null
