{{ config(materialized='view') }}

select
  cast(order_item_id as integer) as order_item_id,
  cast(order_id as integer) as order_id,
  cast(product_id as integer) as product_id,
  cast(quantity as integer) as quantity,
  cast(unit_price as decimal(10,2)) as unit_price,
  cast(coalesce(discount_amount, 0) as decimal(10,2)) as discount_amount,
  current_timestamp as _loaded_at
from {{ source('raw_ecommerce', 'order_items') }}
where order_item_id is not null
  and order_id is not null
  and product_id is not null
  and quantity > 0
