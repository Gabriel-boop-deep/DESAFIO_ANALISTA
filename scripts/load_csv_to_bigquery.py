#!/usr/bin/env python3
"""Load the inspected CSV into BigQuery with normalized snake_case columns."""

from __future__ import annotations

import csv
import re
from pathlib import Path

import chardet
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = PROJECT_ROOT / "DADOS" / "indicador-atendimento-emergencial.csv"
KEYFILE = PROJECT_ROOT / "desafio-analista-499820-978397414cd8.json"
PROJECT_ID = "desafio-analista-499820"
DATASET_ID = "raw_aneel"
TABLE_ID = "indicador_atendimento_emergencial"


def detect_encoding(path: Path) -> str:
    with path.open("rb") as handle:
        return chardet.detect(handle.read(1_000_000)).get("encoding") or "utf-8"


def detect_delimiter(path: Path, encoding: str) -> str:
    with path.open("r", encoding=encoding, newline="") as handle:
        return csv.Sniffer().sniff(handle.read(8192), delimiters=";,|\t").delimiter


def to_snake_case(value: str) -> str:
    normalized = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value.strip())
    normalized = re.sub(r"[^0-9A-Za-z]+", "_", normalized)
    return re.sub(r"_+", "_", normalized).strip("_").lower()


def build_client() -> bigquery.Client:
    credentials = service_account.Credentials.from_service_account_file(KEYFILE)
    return bigquery.Client(project=PROJECT_ID, credentials=credentials)


def ensure_dataset(client: bigquery.Client) -> None:
    dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{DATASET_ID}")
    dataset_ref.location = "US"
    client.create_dataset(dataset_ref, exists_ok=True)


def read_csv_chunks(path: Path, encoding: str, delimiter: str):
    for chunk in pd.read_csv(
        path,
        sep=delimiter,
        encoding=encoding,
        dtype=str,
        keep_default_na=False,
        low_memory=False,
        chunksize=250_000,
    ):
        chunk.columns = [to_snake_case(column) for column in chunk.columns]
        yield chunk


def normalize_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    for column in dataframe.columns:
        dataframe[column] = dataframe[column].astype(str).str.strip()

    if "vlr_indice_enviado" in dataframe.columns:
        dataframe["vlr_indice_enviado_original"] = dataframe["vlr_indice_enviado"]
        dataframe["vlr_indice_enviado"] = (
            dataframe["vlr_indice_enviado"]
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .replace({"": None, "nan": None})
        )
        dataframe["vlr_indice_enviado"] = pd.to_numeric(
            dataframe["vlr_indice_enviado"], errors="coerce"
        )

    for integer_column in ["ano_indice", "num_periodo_indice", "ide_conj_und_consumidoras"]:
        if integer_column in dataframe.columns:
            dataframe[integer_column] = pd.to_numeric(
                dataframe[integer_column].replace({"": None}), errors="coerce"
            ).astype("Int64")

    if "num_cnpj" in dataframe.columns:
        dataframe["num_cnpj"] = dataframe["num_cnpj"].replace({"": None})

    return dataframe


def load_dataframe(
    client: bigquery.Client, dataframe: pd.DataFrame, write_disposition: str
) -> None:
    destination = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    job_config = bigquery.LoadJobConfig(
        write_disposition=write_disposition,
    )
    job = client.load_table_from_dataframe(dataframe, destination, job_config=job_config)
    job.result()


def validate_row_count(client: bigquery.Client, expected_rows: int) -> int:
    query = f"select count(*) as total from `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`"
    result = list(client.query(query).result())
    loaded_rows = int(result[0]["total"])
    if loaded_rows != expected_rows:
        raise ValueError(
            f"Quantidade divergente. Esperado={expected_rows}, carregado={loaded_rows}"
        )
    return loaded_rows


def main() -> None:
    encoding = detect_encoding(CSV_PATH)
    delimiter = detect_delimiter(CSV_PATH, encoding)

    client = build_client()
    ensure_dataset(client)

    total_rows = 0
    for index, chunk in enumerate(read_csv_chunks(CSV_PATH, encoding, delimiter)):
        normalized_chunk = normalize_dataframe(chunk)
        write_disposition = (
            bigquery.WriteDisposition.WRITE_TRUNCATE
            if index == 0
            else bigquery.WriteDisposition.WRITE_APPEND
        )
        load_dataframe(client, normalized_chunk, write_disposition)
        total_rows += len(normalized_chunk)

    loaded_rows = validate_row_count(client, total_rows)

    print("Resumo da carga")
    print(f"- Encoding: {encoding}")
    print(f"- Delimitador: {delimiter}")
    print(f"- Linhas lidas: {total_rows}")
    print(f"- Linhas carregadas: {loaded_rows}")
    print(f"- Destino: {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")


if __name__ == "__main__":
    main()
