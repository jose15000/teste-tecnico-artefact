# Cenário 1: Consulta de Catálogo e Preços

Demonstra a busca de produtos com filtros de categoria e preço máximo, além de consulta pontual de preço e especificações de modelo premium.

---

### Turno 1

**Cliente:** Olá! Quais opções de violões disponíveis vocês têm custando até R$ 1000?

> ⚙️ **Tool Call:** `search_products` com argumentos `{"category":"violão","max_price":1000,"only_in_stock":true,"query":""}`

> 📥 **Tool Result:** `{"total_found": 12, "results": [{"product_id": 83, "name": "Tagima Memphis AC-39 Nylon Natural", "category": "Violões", "price_brl": 429.9, "stock_quantity": 15, "status": "active", "description": "Violão clássico com cordas de nylon, perfeito para quem está começando. Corpo leve e confortável para longas sessões de estudo.", "specs": {"top": "Linden", "back_sides": "Linden", "neck": "Nato", "strings": "nylon", "scale": "650mm", "electronics": "no", "color": "Natural"}}, {"product_id": 85, "name": "Rozini RC-104 Nylon Estudante", "category": "Violões", "price_brl": 459.9, "stock_quantity": 10, "status": "active", "description": "Violão clássico de estudo da Rozini, feito com madeiras nacionais. Acabamento caprichado e preço acessível para iniciantes.", "specs": {"top": "Spruce", "back_sides": "Sapele", "neck": "Nato", "strings": "nylon", "scale": "650mm", "electronics": "no", "color": "Natural"}}, {"product_id": 89, "name": "Shelby SN-100 Folk Aço Preto", "category": "Violões", "price_brl": 549.0, "stock_quantity": 5, "status": "active", "description": "Violão folk aço com visual moderno em preto. Indicado para quem busca um instrumento versátil com boa relação custo-benefício.", "specs": {"top": "Linden", "back_sides": "Linden", "neck": "Nato", "strings": "steel", "scale": "648mm", "electronics": "no", "color": "Preto"}}, {"product_id": 88, "name": "Giannini GF-1R Aço Folk Sunburst", "category": "Violões", "price_brl": 579.9, "stock_quantity": 7, "status": "active", "description": "Violão folk com tampo em Spruce e acabamento Sunburst clássico. Som equilibrado e visual elegante para palco e estúdio.", "specs": {"top": "Spruce", "back_sides": "Sapele", "neck": "Nato", "strings": "steel", "scale": "648mm", "electronics": "no", "color": "Sunburst"}}, {"product_id": 81, "name": "Yamaha C40 Nylon Natural", "category": "Violões", "price_brl": 599.9, "stock_quantity": 12, "status": "active", "description": "Violão clássico com tampo em Spruce e fundo/laterais em Meranti. Ideal para estudantes e iniciantes, com excelente projeção sonora.", "specs": {"top": "Spruce", "back_sides": "Meranti", "neck": "Nato", "strings": "nylon", "scale": "650mm", "electronics": "no", "color": "Natural"}}]}`

**Atendente:**

Oi! Tudo bem? 😊

Segue a lista de violões que temos em estoque por **até R$ 1.000,00**:

| # | Modelo | Tipo de cordas | Preço (R$) | Estoque |
|---|--------|----------------|-----------|---------|
| 1 | **Tagima Memphis AC‑39 Nylon – Natural** | Nylon | 429,90 | 15 |
| 2 | **Rozini RC‑104 Nylon – Estudante** | Nylon | 459,90 | 10 |
| 3 | **Shelby SN‑100 Folk – Preto** | Aço | 549,00 | 5 |
| 4 | **Giannini GF‑1R Folk – Sunburst** | Aço | 579,90 | 7 |
| 5 | **Yamaha C40 – Natural** | Nylon | 599,90 | 12 |

Todos são **ativos** e estão **em estoque**. São ótimas opções para iniciantes e também para quem já toca e quer um instrumento de boa relação custo‑benefício.

Se quiser mais detalhes de algum modelo (especificações, garantia, prazo de entrega etc.) ou quiser fazer a reserva, é só me avisar! 🎸✨

---

### Turno 2

**Cliente:** E quanto custa o Takamine GD20? Vocês têm ele em estoque?

> ⚙️ **Tool Call:** `search_products` com argumentos `{"category":"violões","max_price":null,"only_in_stock":true,"query":"Takamine GD20"}`

> 📥 **Tool Result:** `{"total_found": 1, "results": [{"product_id": 95, "name": "Takamine GD20 Dreadnought Natural", "category": "Violões", "price_brl": 2199.0, "stock_quantity": 5, "status": "active", "description": "Violão dreadnought Takamine com tampo sólido em cedro. Excelente para fingerstyle com timbre quente e definido.", "specs": {"top": "Cedro Sólido", "back_sides": "Sapele", "neck": "Mogno", "strings": "steel", "scale": "650mm", "electronics": "no", "color": "Natural"}}]}`

**Atendente:**

Olá! 😊

O **Takamine GD20 Dreadnought Natural** está disponível em nosso catálogo, porém o preço dele é **R$ 2.199,00**, acima do limite de R$ 1.000,00 que você mencionou anteriormente.

- **Estoque:** 5 unidades
- **Tipo:** Dreadnought, cordas de aço, tampo em cedro sólido

Se o valor estiver dentro do seu orçamento ou se quiser conhecer opções similares que estejam abaixo de R$ 1.000,00, posso sugerir alguns modelos que têm boa qualidade e preço mais acessível. É só me avisar! 🎸

---
