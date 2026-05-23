{%- macro safe_divide(numerator, denominator, default_value = 0) -%}
  case
    when {{ denominator }} != 0 then {{ numerator }} / {{ denominator }}
    else {{ default_value }}
  end
{%- endmacro -%}
