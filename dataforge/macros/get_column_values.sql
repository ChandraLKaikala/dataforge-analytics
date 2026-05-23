{%- macro get_column_values(table, column) -%}
  {%- if execute -%}
    {%- set query = "select distinct " ~ column ~ " from " ~ table ~ " order by " ~ column -%}
    {%- set results = run_query(query) -%}
    {%- if execute -%}
      {%- set values = results.columns[0].values() | list -%}
      {{ return(values) }}
    {%- endif -%}
  {%- endif -%}
{%- endmacro -%}
