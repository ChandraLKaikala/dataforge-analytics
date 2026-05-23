{% snapshot customer_snapshot %}

  {{
    config(
      target_schema='snapshots',
      unique_key='customer_id',
      strategy='timestamp',
      updated_at='updated_at',
    )
  }}

  select
    customer_id,
    email_hash,
    first_name,
    last_name,
    country_code,
    tier,
    created_at,
    current_timestamp as updated_at
  from {{ ref('stg_customers') }}

{% endsnapshot %}
