{% macro get_build_sql(sql, compiled_code, extra_context) %}
  {% if sql == False %}
    {{ compiled_code }}
  {% elif execute %}
    {% if this.meta.get('insert_overwrite', False) %}
      {% set build_sql = compiled_code.replace('create table', 'create or replace table') %}
    {% else %}
      {% set build_sql = compiled_code %}
    {% endif %}
    {{ build_sql }}
  {% endif %}
{% endmacro %}
