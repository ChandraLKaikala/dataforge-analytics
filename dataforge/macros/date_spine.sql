{%- macro create_date_spine() -%}
  {% if execute %}
    {% if 'date_spine' not in graph.nodes.keys() %}
      {% do log('Creating date_spine...', info=True) %}
    {% endif %}
  {% endif %}
{%- endmacro -%}

{%- macro date_spine(start_date, end_date) -%}
  {%- set start = start_date -%}
  {%- set end = end_date -%}
  with date_range as (
    select
      cast({{ dbt.generate_series(start, end, 'day') }} as date) as calendar_date
  )
  select
    calendar_date,
    extract(year from calendar_date) as year,
    extract(month from calendar_date) as month,
    extract(quarter from calendar_date) as quarter,
    extract(week from calendar_date) as week_of_year,
    extract(dayofweek from calendar_date) as day_of_week,
    dayname(calendar_date) as day_name,
    (calendar_date >= current_date) as is_future_date
  from date_range
{%- endmacro -%}
