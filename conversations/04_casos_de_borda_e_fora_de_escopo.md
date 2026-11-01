# Cenário 4: Casos de Borda e Perguntas Fora de Escopo

Demonstra a resposta a produtos sem estoque com sugestão de similares ativos, recusa cordial de venda de acessórios avulsos e redirecionamento de perguntas fora do escopo da loja.

---

### Turno 1

**Cliente:** Olá! Vocês têm o violão Giannini GF-3D Dreadnought Sunburst em estoque?

> ⚙️ **Tool Call:** `search_products` com argumentos `{"query":"Giannini GF-3D Dreadnought Sunburst"}`

> 📥 **Tool Result:** `{"total_found": 1, "results": [{"product_id": 96, "name": "Giannini GF-3D Dreadnought Sunburst", "category": "Violões", "price_brl": 799.9, "stock_quantity": 0, "status": "active", "description": "Violão dreadnought com corpo amplo e acabamento Sunburst. Volume alto e graves profundos, ideal para country e pop.", "specs": {"top": "Spruce", "back_sides": "Sapele", "neck": "Nato", "strings": "steel", "scale": "650mm", "electronics": "no", "color": "Sunburst"}}]}`

> ⚙️ **Tool Call:** `search_products` com argumentos `{"only_in_stock":true,"query":"Giannini dreadnought"}`

> 📥 **Tool Result:** `{"results": [], "message": "Nenhum produto encontrado com esses critérios."}`

> ⚙️ **Tool Call:** `search_products` com argumentos `{"only_in_stock":true,"query":"dreadnought"}`

> 📥 **Tool Result:** `{"total_found": 7, "results": [{"product_id": 107, "name": "Shelby SGD-195E Elétrico Aço Sunburst", "category": "Violões", "price_brl": 799.0, "stock_quantity": 6, "status": "active", "description": "Violão eletroacústico dreadnought com captação e afinador integrado. Boa opção de custo-benefício para quem precisa de amplificação.", "specs": {"top": "Spruce", "back_sides": "Sapele", "neck": "Nato", "strings": "steel", "scale": "650mm", "electronics": "yes", "color": "Sunburst"}}, {"product_id": 91, "name": "Tagima Woodstock Dreadnought Natural", "category": "Violões", "price_brl": 899.0, "stock_quantity": 11, "status": "active", "description": "Violão dreadnought com corpo amplo e som potente. Excelente para fingerpicking e strumming com projeção impressionante.", "specs": {"top": "Spruce", "back_sides": "Sapele", "neck": "Nato", "strings": "steel", "scale": "650mm", "electronics": "no", "color": "Natural"}}, {"product_id": 92, "name": "Yamaha FG800 Dreadnought Natural", "category": "Violões", "price_brl": 1299.0, "stock_quantity": 7, "status": "active", "description": "Violão dreadnought Yamaha com tampo sólido em Spruce. Tecnologia de bracing exclusiva para som rico e encorpado.", "specs": {"top": "Spruce Sólido", "back_sides": "Nato", "neck": "Nato", "strings": "steel", "scale": "650mm", "electronics": "no", "color": "Natural"}}, {"product_id": 95, "name": "Takamine GD20 Dreadnought Natural", "category": "Violões", "price_brl": 2199.0, "stock_quantity": 5, "status": "active", "description": "Violão dreadnought Takamine com tampo sólido em cedro. Excelente para fingerstyle com timbre quente e definido.", "specs": {"top": "Cedro Sólido", "back_sides": "Sapele", "neck": "Mogno", "strings": "steel", "scale": "650mm", "electronics": "no", "color": "Natural"}}, {"product_id": 97, "name": "Crafter D-8 Dreadnought Natural", "category": "Violões", "price_brl": 4599.0, "stock_quantity": 2, "status": "active", "description": "Violão dreadnought premium com tampo sólido em Spruce Sitka e fundo em Rosewood. Acabamento artesanal e som excepcional.", "specs": {"top": "Sitka Spruce Sólido", "back_sides": "Rosewood", "neck": "Mogno", "strings": "steel", "scale": "650mm", "electronics": "no", "color": "Natural"}}]}`

**Atendente:**

Olá! Tudo bem? 😊

Infelizmente o **Giannini GF‑3D Dreadnought Sunburst** está *sem estoque* no momento. 🙁

Mas temos outras opções de violões dreadnought em estoque que podem atender ao seu gosto e ao seu orçamento:

| Modelo | Preço (R$) | Estoque |
|--------|-----------|---------|
| **Tagima Woodstock Dreadnought Natural** | 899,00 | 11 unidades |
| **Yamaha FG800 Dreadnought Natural** | 1 299,00 | 7 unidades |
| **Takamine GD20 Dreadnought Natural** | 2 199,00 | 5 unidades |
| **Crafter D‑8 Dreadnought Natural** (premium) | 4 599,00 | 2 unidades |
| **Shelby SGD‑195E Elétrico Aço Sunburst** (dreadnought eletroacústico) | 799,00 | 6 unidades |

Se quiser mais detalhes de algum desses modelos (especificações, cores, etc.) ou precisar de ajuda para escolher, é só me avisar! Estou à disposição para encontrar o violão perfeito para você. 🎸✨

---

### Turno 2

**Cliente:** Que pena! Tem alguma outra opção parecida folk ou dreadnought Sunburst em estoque na mesma faixa de valor?

> ⚙️ **Tool Call:** `search_products` com argumentos `{"only_in_stock":true,"query":"Sunburst"}`

> 📥 **Tool Result:** `{"total_found": 6, "results": [{"product_id": 119, "name": "Shelby SU-21S Soprano Sunburst", "category": "Ukuleles", "price_brl": 159.9, "stock_quantity": 8, "status": "active", "description": "Ukulele soprano com acabamento Sunburst e escala em Rosewood. Visual clássico e som alegre para músicos de todos os níveis.", "specs": {"top": "Linden", "back_sides": "Linden", "neck": "Nato", "strings": "nylon", "scale": "346mm", "electronics": "no", "color": "Sunburst"}}, {"product_id": 88, "name": "Giannini GF-1R Aço Folk Sunburst", "category": "Violões", "price_brl": 579.9, "stock_quantity": 7, "status": "active", "description": "Violão folk com tampo em Spruce e acabamento Sunburst clássico. Som equilibrado e visual elegante para palco e estúdio.", "specs": {"top": "Spruce", "back_sides": "Sapele", "neck": "Nato", "strings": "steel", "scale": "648mm", "electronics": "no", "color": "Sunburst"}}, {"product_id": 107, "name": "Shelby SGD-195E Elétrico Aço Sunburst", "category": "Violões", "price_brl": 799.0, "stock_quantity": 6, "status": "active", "description": "Violão eletroacústico dreadnought com captação e afinador integrado. Boa opção de custo-benefício para quem precisa de amplificação.", "specs": {"top": "Spruce", "back_sides": "Sapele", "neck": "Nato", "strings": "steel", "scale": "650mm", "electronics": "yes", "color": "Sunburst"}}, {"product_id": 99, "name": "Tagima Classical Elétrico Nylon Sunburst", "category": "Violões", "price_brl": 1199.0, "stock_quantity": 8, "status": "active", "description": "Violão eletroacústico nylon com pré-amplificador e afinador embutido. Versátil para palco e estúdio com excelente resposta tonal.", "specs": {"top": "Spruce", "back_sides": "Sapele", "neck": "Nato", "strings": "nylon", "scale": "650mm", "electronics": "yes", "color": "Sunburst"}}, {"product_id": 145, "name": "Fender Stratocaster American Pro II", "category": "Guitarras", "price_brl": 12500.0, "stock_quantity": 5, "status": "active", "description": "Guitarra elétrica Fender Stratocaster com 3 captadores V-Mod II single-coil. Clássico timbre brilhante e versátil para diversos estilos.", "specs": {"body": "Alder", "neck": "Maple", "strings": "6", "color": "Sunburst"}}]}`

**Atendente:**

Oi, tudo bem? 😊

Temos duas opções **Sunburst** que se encaixam na faixa de preço do Giannini GF‑3D (próxima de R$ 800) e que estão *em estoque*:

| Modelo | Tipo | Preço (R$) | Estoque | Principais specs |
|--------|------|------------|---------|-------------------|
| **Giannini GF‑1R Aço Folk Sunburst** | Folk | **579,90** | 7 unidades | Tampo Spruce, costas/sides Sapele, escala 648 mm, cordas de aço, acabamento Sunburst clássico |
| **Shelby SGD‑195E Elétrico Aço Sunburst** | Dreadnought (eletroacústico) | **799,00** | 6 unidades | Tampo Spruce, costas/sides Sapele, escala 650 mm, captação integrada + afinador, cordas de aço, acabamento Sunburst |

- O **Giannini GF‑1R** tem o formato folk que você mencionou, som equilibrado e visual elegante, ideal para quem busca conforto e boa projeção sem precisar de amplificação.  
- O **Shelby SGD‑195E** oferece o tamanho dreadnought e ainda vem com sistema de captação, caso você queira usá‑lo em shows ou em estúdio.

Se algum desses modelos lhe interessar, posso enviar mais detalhes ou já preparar a reserva para você. É só me falar! 🎸✨

---

### Turno 3

**Cliente:** Vocês vendem também palhetas de nylon e um jogo de cordas avulsas?

**Atendente:**

Oi! 😊

A Empório da Música trabalha **exclusivamente com instrumentos musicais**. Por isso, não comercializamos palhetas, cordas avulsas ou outros acessórios.

Se precisar de um violão, guitarra, baixo, teclado ou outro instrumento, estou à disposição para ajudar a encontrar o modelo perfeito para você! 🎶

---

### Turno 4

**Cliente:** E vocês consertam celular ou micro-ondas aí na loja?

**Atendente:**

Olá! 🙏

A Empório da Música é especializada em **instrumentos musicais** e nos serviços relacionados a eles (venda, manutenção e regulagem de instrumentos). Não realizamos consertos de celulares, micro‑ondas ou outros eletrodomésticos.

Se precisar de algum instrumento ou de assistência para violões, guitarras, baixos, teclados etc., conte comigo! 🎸🎹✨

---
