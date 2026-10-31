from __future__ import annotations

from src.data_loader import load_store_data, normalize_phone, normalize_text

MAX_RESULTS = 5


def _active_discount(store, product_id: int) -> float:
    promos = store.promotions
    row = promos[(promos["product_id"] == product_id) & (promos["is_active"] == 1)]
    return float(row["discount_percent"].max()) if not row.empty else 0.0


def _format_product(store, row) -> dict:
    discount = _active_discount(store, int(row["product_id"]))
    price = float(row["price_brl"])
    item = {
        "product_id": int(row["product_id"]),
        "name": row["name"],
        "category": row["category_name"],
        "price_brl": price,
        "stock_quantity": int(row["stock_quantity"]),
        "status": row["status"],
        "description": row["description"],
        "specs": row["specs_dict"],
    }
    if discount:
        item["discount_percent"] = discount
        item["price_with_discount_brl"] = round(price * (1 - discount / 100), 2)
    return item


def search_products(
    query: str,
    category: str | None = None,
    max_price: float | None = None,
    only_in_stock: bool = False,
) -> dict:
    """Busca produtos no catálogo por texto, categoria e preço."""
    store = load_store_data()
    df = store.products

    terms = normalize_text(query).split()
    for term in terms:
        df = df[df["search_blob"].str.contains(term, regex=False)]
    if category:
        df = df[df["category_name"].apply(normalize_text).str.contains(normalize_text(category), regex=False)]
    if max_price is not None:
        df = df[df["price_brl"] <= max_price]
    if only_in_stock:
        df = df[(df["stock_quantity"] > 0) & (df["status"] == "active")]

    if df.empty:
        return {"results": [], "message": "Nenhum produto encontrado com esses critérios."}

    df = df.sort_values("price_brl")
    return {
        "total_found": len(df),
        "results": [_format_product(store, r) for _, r in df.head(MAX_RESULTS).iterrows()],
    }


def get_order_status(order_id: int, customer_phone: str) -> dict:
    """Consulta o status de um pedido, validando o telefone do cliente dono do pedido."""
    store = load_store_data()

    order = store.orders[store.orders["order_id"] == int(order_id)]
    if order.empty:
        return {"error": "Pedido não encontrado para este telefone."}
    order = order.iloc[0]

    customer = store.customers[store.customers["customer_id"] == order["customer_id"]].iloc[0]
    if normalize_phone(customer_phone) != customer["phone_digits"]:
        # Mesma mensagem do "não encontrado" para não vazar a existência do pedido.
        return {"error": "Pedido não encontrado para este telefone."}

    items = store.order_items[store.order_items["order_id"] == order["order_id"]].merge(
        store.products[["product_id", "name"]], on="product_id", how="left"
    )
    return {
        "order_id": int(order["order_id"]),
        "customer_name": customer["name"],
        "order_date": order["order_date"],
        "status": order["status"],
        "total_brl": float(order["total_brl"]),
        "payment_method": order["payment_method"],
        "tracking_code": order["tracking_code"] or None,
        "estimated_delivery": order["estimated_delivery"] or None,
        "notes": order["notes"] or None,
        "items": [{"name": r["name"], "quantity": int(r["quantity"])} for _, r in items.iterrows()],
    }


AVAILABLE_TOOLS = {
    "search_products": search_products,
    "get_order_status": get_order_status,
}
