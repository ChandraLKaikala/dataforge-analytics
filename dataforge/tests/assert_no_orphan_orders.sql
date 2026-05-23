-- Test: Detect orphan orders with no customer in the customer dimension
select
  order_id,
  customer_id
from {{ ref('stg_orders') }}
where customer_id not in (select customer_id from {{ ref('stg_customers') }})
