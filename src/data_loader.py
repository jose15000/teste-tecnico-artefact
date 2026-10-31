from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def normalize_text(text: str | None) -> str:
    """Remove acentos, converte para minúsculas e remove espaços extras."""
    if not text or not isinstance(text, str):
        return ""
    nfkd = unicodedata.normalize("NFKD", text)
    without_accents = "".join(c for c in nfkd if not unicodedata.combining(c))
    return without_accents.lower().strip()


def normalize_phone(phone: str | None) -> str:
    """Mantém apenas os dígitos numéricos de um telefone."""
    if not phone or not isinstance(phone, str):
        return ""
    return re.sub(r"\D", "", phone)


def _resolve_file(data_dir: Path, candidates: list[str]) -> Path:
    """Localiza o arquivo na pasta data aceitando múltiplos nomes possíveis."""
    for name in candidates:
        path = data_dir / name
        if path.exists():
            return path
    raise FileNotFoundError(
        f"Nenhum dos arquivos esperados {candidates} foi encontrado em {data_dir}"
    )


def _parse_specs(raw_specs: Any) -> dict[str, Any]:
    """Converte a coluna JSON 'specs' em dicionário Python de forma segura."""
    if not isinstance(raw_specs, str) or not raw_specs.strip():
        return {}
    try:
        return json.loads(raw_specs)
    except json.JSONDecodeError:
        return {}


@dataclass
class StoreData:
    products: pd.DataFrame
    categories: pd.DataFrame
    promotions: pd.DataFrame
    orders: pd.DataFrame
    order_items: pd.DataFrame
    customers: pd.DataFrame
    policies_pdf_path: Path


@lru_cache(maxsize=1)
def load_store_data(data_dir: Path = DATA_DIR) -> StoreData:
    """Carrega, valida e pré-processa todos os CSVs e localiza o PDF de políticas."""
    categories_path = _resolve_file(
        data_dir, ["categories.csv", "desafio_tecnico_ai_eng - categories.csv"]
    )
    customers_path = _resolve_file(
        data_dir, ["customers.csv", "desafio_tecnico_ai_eng - customers.csv"]
    )
    order_items_path = _resolve_file(
        data_dir, ["order_items.csv", "desafio_tecnico_ai_eng - order_items.csv"]
    )
    orders_path = _resolve_file(
        data_dir, ["orders.csv", "desafio_tecnico_ai_eng - orders.csv"]
    )
    products_path = _resolve_file(
        data_dir, ["products.csv", "desafio_tecnico_ai_eng - products.csv"]
    )
    promotions_path = _resolve_file(
        data_dir, ["promotions.csv", "desafio_tecnico_ai_eng - promotions.csv"]
    )
    policies_pdf_path = _resolve_file(
        data_dir, ["politicas_da_loja.pdf", "políticas_da_loja.pdf"]
    )

    categories_df = pd.read_csv(categories_path)
    customers_df = pd.read_csv(customers_path)
    order_items_df = pd.read_csv(order_items_path)
    orders_df = pd.read_csv(orders_path)
    products_df = pd.read_csv(products_path)
    promotions_df = pd.read_csv(promotions_path)

    # Pré-processamento de categorias
    categories_df["category_id"] = categories_df["category_id"].astype(int)
    categories_df["name_norm"] = categories_df["name"].apply(normalize_text)

    # Pré-processamento de produtos + join com nome da categoria
    products_df["product_id"] = products_df["product_id"].astype(int)
    products_df["category_id"] = products_df["category_id"].astype(int)
    products_df["price_brl"] = products_df["price_brl"].astype(float)
    products_df["stock_quantity"] = products_df["stock_quantity"].astype(int)
    products_df["status"] = products_df["status"].astype(str).str.strip()
    products_df["specs_dict"] = products_df["specs"].apply(_parse_specs)

    products_df = products_df.merge(
        categories_df[["category_id", "name"]].rename(columns={"name": "category_name"}),
        on="category_id",
        how="left",
    )

    # Campos normalizados para busca textual rápida e sem acentos
    products_df["search_blob"] = (
        products_df["name"].fillna("")
        + " "
        + products_df["description"].fillna("")
        + " "
        + products_df["category_name"].fillna("")
        + " "
        + products_df["specs"].fillna("")
    ).apply(normalize_text)

    # Pré-processamento de promoções
    promotions_df["promotion_id"] = promotions_df["promotion_id"].astype(int)
    promotions_df["product_id"] = promotions_df["product_id"].astype(int)
    promotions_df["discount_percent"] = promotions_df["discount_percent"].astype(float)
    promotions_df["is_active"] = promotions_df["is_active"].astype(int)

    # Pré-processamento de clientes
    customers_df["customer_id"] = customers_df["customer_id"].astype(int)
    customers_df["name_norm"] = customers_df["name"].apply(normalize_text)
    customers_df["phone_digits"] = customers_df["phone"].apply(normalize_phone)

    # Pré-processamento de pedidos e itens
    orders_df["order_id"] = orders_df["order_id"].astype(int)
    orders_df["customer_id"] = orders_df["customer_id"].astype(int)
    orders_df["total_brl"] = orders_df["total_brl"].astype(float)
    for col in ["tracking_code", "estimated_delivery", "notes"]:
        orders_df[col] = orders_df[col].fillna("").astype(str).str.strip()

    order_items_df["order_id"] = order_items_df["order_id"].astype(int)
    order_items_df["product_id"] = order_items_df["product_id"].astype(int)
    order_items_df["quantity"] = order_items_df["quantity"].astype(int)

    return StoreData(
        products=products_df,
        categories=categories_df,
        promotions=promotions_df,
        orders=orders_df,
        order_items=order_items_df,
        customers=customers_df,
        policies_pdf_path=policies_pdf_path,
    )
