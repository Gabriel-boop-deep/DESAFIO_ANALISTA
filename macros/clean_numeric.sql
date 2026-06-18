{% macro clean_numeric(column_name) -%}
safe_cast(
  nullif(
    replace(
      replace(trim(cast({{ column_name }} as string)), '.', ''),
      ',',
      '.'
    ),
    ''
  ) as float64
)
{%- endmacro %}

