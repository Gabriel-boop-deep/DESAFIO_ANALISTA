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
        percentil_performance,
        quartil_performance,
        total_distribuidoras_periodo,
        tmae_benchmark_nacional,
        tmae_limite_top_10,
        score_performance
    from {{ ref('int_tmae_ranking') }}
),

evolucao as (
    select
        distribuidora,
        data_referencia,
        tmae_mes_anterior,
        tmae_ano_anterior,
        variacao_abs_mes_anterior,
        variacao_pct_mes_anterior,
        variacao_abs_ano_anterior,
        variacao_pct_ano_anterior,
        media_movel_3m,
        tendencia,
        tendencia_anual
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
    benchmarks.desvio_padrao_tmae_brasil,
    benchmarks.menor_tmae_brasil,
    benchmarks.maior_tmae_brasil,
    benchmarks.quantidade_distribuidoras_brasil,
    benchmarks.media_tmae_regiao,
    benchmarks.media_tmae_grupo,
    b.tmae - benchmarks.media_tmae_brasil as diferenca_vs_brasil,
    safe_divide(b.tmae - benchmarks.media_tmae_brasil, benchmarks.media_tmae_brasil) as diferenca_percentual_vs_brasil,
    b.tmae - benchmarks.media_tmae_regiao as diferenca_vs_regiao,
    safe_divide(b.tmae - benchmarks.media_tmae_regiao, benchmarks.media_tmae_regiao) as diferenca_percentual_vs_regiao,
    b.tmae - benchmarks.media_tmae_grupo as diferenca_vs_grupo,
    safe_divide(b.tmae - benchmarks.media_tmae_grupo, benchmarks.media_tmae_grupo) as diferenca_percentual_vs_grupo,
    ranking.ranking_nacional,
    ranking.ranking_regional,
    ranking.ranking_grupo,
    ranking.percentil_performance,
    ranking.quartil_performance,
    ranking.total_distribuidoras_periodo,
    evolucao.tmae_mes_anterior,
    evolucao.tmae_ano_anterior,
    evolucao.variacao_abs_mes_anterior,
    evolucao.variacao_pct_mes_anterior,
    evolucao.variacao_abs_ano_anterior,
    evolucao.variacao_pct_ano_anterior,
    evolucao.media_movel_3m,
    evolucao.tendencia,
    evolucao.tendencia_anual,
    {{ classify_performance('b.tmae', 'benchmarks.media_tmae_brasil') }} as classificacao_performance,
    safe_divide(
        b.tmae - benchmarks.media_tmae_brasil,
        nullif(benchmarks.desvio_padrao_tmae_brasil, 0)
    ) as zscore_tmae_brasil,
    abs(
        safe_divide(
            b.tmae - benchmarks.media_tmae_brasil,
            nullif(benchmarks.desvio_padrao_tmae_brasil, 0)
        )
    ) >= 2 as flag_outlier_tmae,
    ranking.ranking_nacional <= 10 as flag_top_10_melhores,
    ranking.ranking_nacional >= greatest(benchmarks.quantidade_distribuidoras_brasil - 9, 1) as flag_top_10_piores,
    ranking.tmae_benchmark_nacional,
    ranking.tmae_limite_top_10,
    b.tmae - ranking.tmae_benchmark_nacional as distancia_para_benchmark,
    b.tmae - ranking.tmae_limite_top_10 as distancia_para_top_10,
    ranking.score_performance,
    case
        when b.flag_neoenergia_coelba and evolucao.variacao_abs_mes_anterior < 0 then 'Coelba melhorando'
        when b.flag_neoenergia_coelba and evolucao.variacao_abs_mes_anterior > 0 then 'Coelba piorando'
        when b.flag_neoenergia_coelba then 'Coelba estavel'
        else 'Nao se aplica'
    end as status_coelba_mes,
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
