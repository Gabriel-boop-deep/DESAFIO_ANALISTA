{% macro classify_performance(tmae_expression, media_brasil_expression) -%}
case
  when {{ tmae_expression }} is null or {{ media_brasil_expression }} is null then 'Sem classificacao'
  when {{ tmae_expression }} <= {{ media_brasil_expression }} * 0.85 then 'Excelente'
  when {{ tmae_expression }} <= {{ media_brasil_expression }} then 'Bom'
  when {{ tmae_expression }} <= {{ media_brasil_expression }} * 1.15 then 'Atencao'
  else 'Critico'
end
{%- endmacro %}
