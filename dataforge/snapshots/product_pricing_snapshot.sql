{% snapshot product_pricing_snapshot %}

  {{
    config(
      target_schema='snapshots',
      unique_key='product_id',
      strategy='timestamp',
      updated_at='price_updated_at',
    )
  }}

  select
    product_id,
    name,
    category,
    price,
    cost,
    active,
    current_timestamp as price_updated_at
  from {{ ref('stg_products') }}

{% endsnapshot %}
