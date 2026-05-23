{{ config(materialized='view') }}

select
  cast(product_id as integer) as product_id,
  cast(name as varchar) as name,
  cast(category as varchar) as category,
  cast(price as decimal(10,2)) as price,
  cast(cost as decimal(10,2)) as cost,
  cast(active as boolean) as active,
  current_timestamp as _loaded_at
from {{ source('raw_ecommerce', 'products') }}
where product_id is not null
  and name is not null
