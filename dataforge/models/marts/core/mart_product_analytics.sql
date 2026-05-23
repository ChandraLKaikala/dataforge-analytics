{{ config(
    materialized='table',
    contract={
        'enforced': true,
        'columns': [
            {'name': 'product_id', 'data_type': 'integer'},
            {'name': 'product_name', 'data_type': 'varchar'},
            {'name': 'category', 'data_type': 'varchar'},
            {'name': 'total_revenue', 'data_type': 'decimal'},
            {'name': 'total_units_sold', 'data_type': 'integer'},
            {'name': 'gross_profit', 'data_type': 'decimal'},
            {'name': 'order_count', 'data_type': 'integer'},
            {'name': 'avg_unit_price', 'data_type': 'decimal'},
            {'name': 'profit_margin_percent', 'data_type': 'decimal'},
        ]
    }
) }}

select
  pp.product_id,
  pp.name as product_name,
  pp.category,
  coalesce(pp.total_revenue, 0) as total_revenue,
  coalesce(pp.total_units_sold, 0) as total_units_sold,
  coalesce(pp.gross_profit, 0) as gross_profit,
  coalesce(pp.order_count, 0) as order_count,
  coalesce(pp.avg_unit_price, 0) as avg_unit_price,
  {{ safe_divide('coalesce(pp.gross_profit, 0)', 'coalesce(pp.total_revenue, 1)', 0) }} * 100 as profit_margin_percent
from {{ ref('int_product_performance') }} pp
