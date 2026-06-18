{% macro classify_performance(tmae_expression, media_brasil_expression) -%}
case
  when {{ tmae_expression }} <= {{ media_brasil_expression }} then 'Melhor que a media nacional'
  when {{ tmae_expression }} <= {{ media_brasil_expression }} * 1.10 then 'Proximo da media nacional'
  else 'Pior que a media nacional'
end
{%- endmacro %}

