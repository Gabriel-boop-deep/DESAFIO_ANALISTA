#!/usr/bin/env python3
"""Inspect the ANEEL emergency attendance CSV and write a markdown report."""

from __future__ import annotations

import csv
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import chardet


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "DADOS" / "indicador-atendimento-emergencial.csv"
REPORT_PATH = PROJECT_ROOT / "docs_inspecao_csv.md"
SAMPLE_ROWS = 5
ENCODING_BYTES = 1_000_000


@dataclass
class ColumnProfile:
    name: str
    non_null: int = 0
    nulls: int = 0
    numeric_like: int = 0
    decimal_comma: int = 0
    date_like: int = 0
    max_len: int = 0
    samples: list[str] | None = None

    def __post_init__(self) -> None:
        if self.samples is None:
            self.samples = []


def detect_encoding(path: Path) -> str:
    with path.open("rb") as handle:
        raw = handle.read(ENCODING_BYTES)
    detected = chardet.detect(raw)
    return detected.get("encoding") or "utf-8"


def detect_delimiter(path: Path, encoding: str) -> str:
    with path.open("r", encoding=encoding, newline="") as handle:
        sample = handle.read(8192)
    return csv.Sniffer().sniff(sample, delimiters=";,|\t").delimiter


def to_snake_case(value: str) -> str:
    normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value.strip())
    normalized = re.sub(r"[^0-9A-Za-z]+", "_", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_").lower()
    return normalized


def infer_semantic_role(column_name: str, values: Iterable[str]) -> str:
    joined = " ".join(v.upper() for v in values if v)
    column_upper = column_name.upper()
    if "SIGAGENTE" in column_upper:
        return "distribuidora"
    if "NUMCNPJ" in column_upper:
        return "cnpj"
    if "IDECONJ" in column_upper:
        return "id_conjunto"
    if "DSCCONJ" in column_upper:
        return "descricao_conjunto"
    if "SIGINDICADOR" in column_upper:
        return "tipo_indicador"
    if "ANOINDICE" in column_upper:
        return "ano"
    if "NUMPERIODOINDICE" in column_upper:
        return "mes"
    if "VLRINDICEENVIADO" in column_upper:
        if "TMP" in joined and "TMD" in joined:
            return "valor_indicador"
        return "valor_numerico"
    if "DATGERACAO" in column_upper:
        return "data_geracao"
    return "nao_identificado"


def infer_type(profile: ColumnProfile) -> str:
    ratio = lambda x: x / profile.non_null if profile.non_null else 0.0
    if ratio(profile.date_like) > 0.9:
        return "date_string"
    if ratio(profile.numeric_like) > 0.9:
        if profile.decimal_comma:
            return "numeric_string_decimal_comma"
        return "numeric_string"
    return "string"


def main() -> None:
    encoding = detect_encoding(CSV_PATH)
    delimiter = detect_delimiter(CSV_PATH, encoding)

    with CSV_PATH.open("r", encoding=encoding, newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        columns = reader.fieldnames or []
        profiles = {column: ColumnProfile(name=column) for column in columns}
        total_rows = 0
        preview: list[dict[str, str]] = []
        indicators = Counter()
        agents = Counter()
        malformed_rows = 0

        for row in reader:
            if None in row:
                malformed_rows += 1
            total_rows += 1
            if len(preview) < SAMPLE_ROWS:
                preview.append(row)

            indicator = (row.get("SigIndicador") or "").strip()
            agent = (row.get("SigAgente") or "").strip()
            if indicator:
                indicators[indicator] += 1
            if agent:
                agents[agent] += 1

            for column in columns:
                value = (row.get(column) or "").strip()
                profile = profiles[column]
                if value == "":
                    profile.nulls += 1
                    continue

                profile.non_null += 1
                profile.max_len = max(profile.max_len, len(value))
                if len(profile.samples) < 5 and value not in profile.samples:
                    profile.samples.append(value)

                number_candidate = value.replace(".", "").replace(",", ".")
                if re.fullmatch(r"-?\d+(?:\.\d+)?", number_candidate):
                    profile.numeric_like += 1
                    if "," in value:
                        profile.decimal_comma += 1

                if re.fullmatch(r"\d{2}-\d{2}-\d{4}", value):
                    profile.date_like += 1

    numeric_columns = [
        column
        for column, profile in profiles.items()
        if infer_type(profile).startswith("numeric")
    ]
    decimal_columns = [
        column for column, profile in profiles.items() if profile.decimal_comma > 0
    ]

    semantic_mapping = {
        column: infer_semantic_role(column, profile.samples or [])
        for column, profile in profiles.items()
    }
    snake_case_mapping = {column: to_snake_case(column) for column in columns}

    lines = [
        "# Inspecao do CSV de Atendimento Emergencial",
        "",
        "## Resumo",
        f"- Arquivo: `{CSV_PATH}`",
        f"- Encoding detectado: `{encoding}`",
        f"- Separador detectado: `{delimiter}`",
        f"- Quantidade de linhas de dados: `{total_rows}`",
        f"- Quantidade de colunas: `{len(columns)}`",
        f"- Linhas potencialmente malformadas: `{malformed_rows}`",
        "",
        "## Colunas reais",
        "",
        "| Coluna original | Snake case sugerido | Tipo inferido | Nulos | Max len | Papel sugerido |",
        "|---|---|---|---:|---:|---|",
    ]

    for column in columns:
        profile = profiles[column]
        lines.append(
            f"| {column} | {snake_case_mapping[column]} | {infer_type(profile)} | "
            f"{profile.nulls} | {profile.max_len} | {semantic_mapping[column]} |"
        )

    lines.extend(
        [
            "",
            "## Primeiras linhas",
            "",
            "```python",
        ]
    )
    for row in preview:
        lines.append(str(row))
    lines.extend(["```", "", "## Nulos por coluna", ""])
    for column in columns:
        lines.append(f"- `{column}`: {profiles[column].nulls}")

    lines.extend(
        [
            "",
            "## Colunas numericas detectadas",
            "",
            f"- {', '.join(f'`{name}`' for name in numeric_columns)}",
            "",
            "## Colunas com virgula decimal",
            "",
            f"- {', '.join(f'`{name}`' for name in decimal_columns)}",
            "",
            "## Indicadores encontrados",
            "",
        ]
    )
    for indicator, count in indicators.most_common():
        lines.append(f"- `{indicator}`: {count}")

    lines.extend(
        [
            "",
            "## Distribuidoras mais frequentes",
            "",
        ]
    )
    for agent, count in agents.most_common(15):
        lines.append(f"- `{agent}`: {count}")

    lines.extend(
        [
            "",
            "## Mapeamento tecnico sugerido",
            "",
            "- `SigAgente` representa a distribuidora/agente regulado.",
            "- `AnoIndice` e `NumPeriodoIndice` representam ano e mes de competencia.",
            "- `SigIndicador` define o tipo de indicador, exigindo pivot em dbt.",
            "- `VlrIndiceEnviado` armazena o valor do indicador em formato brasileiro.",
            "- `TMM` sera tratado como proxy operacional de `TMAE`, pois o CSV real nao traz `TMAE` como sigla.",
            "- `NumOcorr` permite derivar `quantidade_ocorrencias`.",
            "- `tempo_total_atendimento` pode ser estimado por `tmae * quantidade_ocorrencias`.",
            "",
            "## Campos equivalentes solicitados",
            "",
            "- distribuidora: `SigAgente`",
            "- uf: nao existe explicitamente no CSV; sera derivada por regra heuristica",
            "- regiao: nao existe explicitamente no CSV; sera derivada a partir da UF quando possivel",
            "- grupo_economico: nao existe explicitamente no CSV; sera derivado por padrao do nome da distribuidora",
            "- ano: `AnoIndice`",
            "- mes: `NumPeriodoIndice`",
            "- tmp: `SigIndicador = TMP`",
            "- tmd: `SigIndicador = TMD`",
            "- tme: `SigIndicador = TME`",
            "- tmae: `SigIndicador = TMM` (decisao documentada)",
            "",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Encoding: {encoding}")
    print(f"Delimiter: {delimiter}")
    print(f"Rows: {total_rows}")
    print(f"Columns: {len(columns)}")
    print(f"Numeric columns: {numeric_columns}")
    print(f"Decimal comma columns: {decimal_columns}")
    print(f"Report written to: {REPORT_PATH}")


if __name__ == "__main__":
    main()

