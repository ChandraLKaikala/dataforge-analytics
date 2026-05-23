{%- macro generate_surrogate_key(column_list) -%}
  {%- if execute -%}
    md5(concat_ws('|', {% for col in column_list %}cast({{ col }} as varchar){{ ',' if not loop.last else '' }}{% endfor %}))
  {%- endif -%}
{%- endmacro -%}
