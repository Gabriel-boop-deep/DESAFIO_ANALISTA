with base as (
    select * from {{ ref('int_tmae_base_calculada') }}
),

benchmarks as (
    select * from {{ ref('int_tmae_benchmarks') }}
),

ranking as (
    select
        distribuidora,
        data_referencia,
        ranking_nacional,
        ranking_regional,
        ranking_grupo,
        percentil_performance
    from {{ ref('int_tmae_ranking') }}
),

evolucao as (
    select
        distribuidora,
        data_referencia,
        tmae_mes_anterior,
        variacao_abs_mes_anterior,
        variacao_pct_mes_anterior,
        media_movel_3m,
        tendencia
    from {{ ref('int_tmae_evolucao') }}
)

select
    b.data_referencia,
    b.ano,
    b.mes,
    format_date('%Y-%m', b.data_referencia) as ano_mes,
    b.distribuidora,
    b.sigla_distribuidora,
    b.uf,
    b.regiao,
    b.grupo_economico,
    b.quantidade_conjuntos,
    b.tmp,
    b.tmd,
    b.tme,
    b.tmae,
    b.tmae_calculado,
    b.diferenca_tmae_calculado,
    b.flag_tmae_inconsistente,
    b.quantidade_ocorrencias,
    b.tempo_total_atendimento,
    benchmarks.media_tmae_brasil,
    benchmarks.media_tmae_regiao,
    benchmarks.media_tmae_grupo,
    b.tmae - benchmarks.media_tmae_brasil as diferenca_vs_brasil,
    safe_divide(b.tmae - benchmarks.media_tmae_brasil, benchmarks.media_tmae_brasil) as diferenca_percentual_vs_brasil,
    ranking.ranking_nacional,
    ranking.ranking_regional,
    ranking.ranking_grupo,
    ranking.percentil_performance,
    evolucao.tmae_mes_anterior,
    evolucao.variacao_abs_mes_anterior,
    evolucao.variacao_pct_mes_anterior,
    evolucao.media_movel_3m,
    evolucao.tendencia,
    {{ classify_performance('b.tmae', 'benchmarks.media_tmae_brasil') }} as classificacao_performance,
    b.participacao_tmp,
    b.participacao_tmd,
    b.participacao_tme,
    b.principal_componente_tmae,
    benchmarks.melhor_distribuidora_periodo,
    benchmarks.pior_distribuidora_periodo,
    benchmarks.benchmark_nacional,
    b.flag_neoenergia_coelba,
    b.flag_registro_valido
from base b
left join benchmarks
    on b.distribuidora = benchmarks.distribuidora
   and b.data_referencia = benchmarks.data_referencia
   and b.regiao = benchmarks.regiao
   and b.grupo_economico = benchmarks.grupo_economico
left join ranking
    on b.distribuidora = ranking.distribuidora
   and b.data_referencia = ranking.data_referencia
left join evolucao
    on b.distribuidora = evolucao.distribuidora
   and b.data_referencia = evolucao.data_referencia
