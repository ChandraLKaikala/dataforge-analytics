{{ config(materialized='view') }}

select
  cast(order_id as integer) as order_id,
  cast(customer_id as integer) as customer_id,
  cast(order_date as timestamp) as order_date,
  cast(total_amount as decimal(10,2)) as total_amount,
  cast(status as varchar) as status,
  cast(payment_method as varchar) as payment_method,
  current_timestamp as _loaded_at
from {{ source('raw_ecommerce', 'orders') }}
where order_id is not null
  and customer_id is not null
  and order_date is not null
