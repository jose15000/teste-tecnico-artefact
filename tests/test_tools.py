from __future__ import annotations

import pytest

from src.tools import AVAILABLE_TOOLS, get_order_status, search_policies, search_products
from src.tools_schema import TOOLS_SCHEMA


def test_tools_schema_and_available_tools_match():
    schema_names = {t["function"]["name"] for t in TOOLS_SCHEMA}
    assert schema_names == set(AVAILABLE_TOOLS.keys())
    assert "search_products" in AVAILABLE_TOOLS
    assert "get_order_status" in AVAILABLE_TOOLS
    assert "search_policies" in AVAILABLE_TOOLS


class TestSearchProducts:
    def test_search_by_query_finds_item(self):
        result = search_products("Yamaha C40")
        assert result.get("total_found", 0) > 0
        first = result["results"][0]
        assert "Yamaha" in first["name"]
        assert "price_brl" in first
        assert "stock_quantity" in first

    def test_search_with_category_filter(self):
        result = search_products("violão", category="Violões")
        assert result.get("total_found", 0) > 0
        for item in result["results"]:
            assert item["category"] == "Violões"

    def test_search_with_singular_category_filter(self):
        result = search_products("aço", category="violão")
        assert result.get("total_found", 0) > 0
        for item in result["results"]:
            assert item["category"] == "Violões"

    def test_search_with_max_price(self):
        max_price = 1000.0
        result = search_products("violão", max_price=max_price)
        assert result.get("total_found", 0) > 0
        for item in result["results"]:
            assert item["price_brl"] <= max_price

    def test_search_not_found(self):
        result = search_products("produto_totalmente_inexistente_xyz_123")
        assert result.get("results") == []
        assert "Nenhum produto encontrado" in result.get("message", "")


class TestGetOrderStatus:
    def test_valid_order_and_phone(self):
        # Pedido 1 pertence ao cliente 3 com telefone (67) 98432-1098
        result = get_order_status(order_id=1, customer_phone="(67) 98432-1098")
        assert "error" not in result
        assert result["order_id"] == 1
        assert result["customer_name"] == "Pedro Henrique Oliveira"
        assert "items" in result
        assert len(result["items"]) > 0

    def test_phone_mismatch_returns_generic_error(self):
        # Telefone divergente do dono do pedido
        result = get_order_status(order_id=1, customer_phone="(67) 99999-9999")
        assert "error" in result
        assert result["error"] == "Pedido não encontrado para este telefone."

    def test_nonexistent_order_returns_generic_error(self):
        result = get_order_status(order_id=999999, customer_phone="(67) 98432-1098")
        assert "error" in result
        assert result["error"] == "Pedido não encontrado para este telefone."


class TestSearchPolicies:
    def test_empty_query_returns_error(self):
        result = search_policies("")
        assert "error" in result

        result_whitespace = search_policies("   ")
        assert "error" in result_whitespace

    def test_freight_in_campo_grande(self):
        result = search_policies("qual o prazo de entrega em Campo Grande?")
        assert result.get("total_found", 0) > 0
        top_titles = [r["title"] for r in result["results"]]
        assert any("Campo Grande" in t or "Frete" in t for t in top_titles)
        # Deve mencionar frete grátis ou motoboy ou taxa
        all_content = " ".join(r["content"] for r in result["results"])
        assert "Campo Grande" in all_content
        assert "500" in all_content or "35" in all_content

    def test_exchange_and_return_policy(self):
        result = search_policies("como funciona troca por defeito ou devolução?")
        assert result.get("total_found", 0) > 0
        all_content = " ".join(r["content"] for r in result["results"])
        assert "troca" in all_content.lower() or "defeito" in all_content.lower()
        assert "dias" in all_content.lower()

    def test_store_hours(self):
        result = search_policies("qual o horário de funcionamento?")
        assert result.get("total_found", 0) > 0
        all_content = " ".join(r["content"] for r in result["results"])
        assert "Horário de Funcionamento" in all_content
        assert "09:00" in all_content

    def test_payment_and_pix_discount(self):
        result = search_policies("quais as formas de pagamento e desconto no pix?")
        assert result.get("total_found", 0) > 0
        all_content = " ".join(r["content"] for r in result["results"])
        assert "PIX" in all_content
        assert "5%" in all_content
