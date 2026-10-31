TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": (
                "Busca instrumentos no catálogo da loja. Retorna preço, estoque, status "
                "(active, discontinued, coming_soon), specs e promoção ativa."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Palavras-chave do produto, ex: 'violão nylon' ou 'Yamaha'.",
                    },
                    "category": {
                        "type": "string",
                        "description": "Categoria opcional, ex: 'Guitarras', 'Baixos', 'Ukuleles'.",
                    },
                    "max_price": {"type": "number", "description": "Preço máximo em reais."},
                    "only_in_stock": {
                        "type": "boolean",
                        "description": "Se true, retorna apenas produtos ativos com estoque.",
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": (
                "Consulta status, rastreio e itens de um pedido. Exige o número do pedido "
                "e o telefone do cliente para confirmar a identidade."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer", "description": "Número do pedido."},
                    "customer_phone": {
                        "type": "string",
                        "description": "Telefone cadastrado do cliente, ex: (67) 99812-3456.",
                    },
                },
                "required": ["order_id", "customer_phone"],
            },
        },
    },
]
