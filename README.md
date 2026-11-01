# Teste Técnico Artefact — Atendente Virtual da Empório da Música

Agente de atendimento (estilo WhatsApp) para uma loja de instrumentos musicais em Campo Grande/MS. Usa LLM via **Groq** com *tool calling* sobre os dados da loja (CSVs).

## Como executar

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencha GROQ_API_KEY
python main.py
```

Comandos no chat: `sair` encerra, `limpar` reinicia a conversa.

Testes: `pytest`

## Configuração (`.env`)

| Variável | Descrição |
|---|---|
| `GROQ_API_KEY` | Chave da API Groq (obrigatória) |
| `GROQ_MODEL` | Modelo (padrão `openai/gpt-oss-120b`) |
| `EMBEDDING_MODEL` | Modelo de embeddings local (para a RAG de políticas) |

## Arquitetura

```
main.py                CLI interativa
src/agent.py           Loop de tool calling com a Groq
src/prompts.py         System prompt e regras de negócio
src/tools.py           Ferramentas: search_products, get_order_status, search_policies
src/tools_schema.py    Schemas JSON das ferramentas para o LLM
src/data_loader.py     Carga e normalização dos CSVs
src/rag.py             Busca híbrida nas políticas da loja (PDF)
data/                  CSVs e PDF de políticas
tests/                 Testes das ferramentas
```

## Detalhes da implementação

### Agente ([src/agent.py](src/agent.py))
- Mantém o histórico de mensagens, iniciado com o system prompt.
- `chat()` roda um loop de até `max_steps` (5): chama o modelo, executa as tool calls solicitadas, devolve os resultados como mensagens `tool` e repete até haver resposta final em texto.
- Erros de ferramenta são devolvidos ao modelo como dados (`{"error": ...}`), permitindo que ele se corrija.
- **Robustez:** o modelo às vezes escreve o raciocínio em texto em vez de gerar o tool call, e a Groq responde `400 output_parse_failed`. `_create_with_retry` repete a chamada até 3 vezes nesse caso; se ainda falhar, retorna uma mensagem de fallback. Outros erros 400 são propagados.

### Ferramentas ([src/tools.py](src/tools.py))
- **`search_products`**: busca por texto (todos os termos, sem acento/caixa), com filtros de categoria, preço máximo e apenas em estoque. Ordena por preço, retorna até 5 resultados e inclui promoção ativa (`discount_percent`, `price_with_discount_brl`).
- **`get_order_status`**: consulta pedido exigindo o telefone do cliente. Telefone divergente e pedido inexistente retornam a mesma mensagem, para não vazar a existência de pedidos.
- **`search_policies`**: busca híbrida no manual de políticas da loja (PDF) para dúvidas sobre fretes, prazos de entrega, trocas e devoluções, formas de pagamento, regras de parcelamento, garantia e horários.

### RAG e Políticas ([src/rag.py](src/rag.py))
- **Extração & Chunking estruturado**: extrai o texto do PDF via `PyMuPDF`, limpando cabeçalhos repetitivos e numerações de página. Segmenta hierarquicamente por seções e subseções numeradas (1 a 10 e subitens como 5.1, 5.2), preservando o título da seção pai em cada trecho (ex.: `5. Política de Frete e Entregas — 5.1 Entregas na Região Metropolitana de Campo Grande`).
- **Indexação 100% em Memória RAM**: gera os chunks e a matriz de embeddings uma única vez via padrão singleton com lazy-loading (`get_policy_retriever()`), evitando recálculos e dependência de bancos vetoriais pesados.
- **Busca Híbrida (Densa + Léxica)**:
  - *Densa*: embeddings multilingues locais via `fastembed` (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` em ONNX Runtime) normalizados em L2, calculando similaridade de cosseno via produto escalar (`np.dot`) em microssegundos.
  - *Léxica*: correspondência de termos exatos com pesos diferenciados (bônus no título e no conteúdo), garantindo precisão em termos críticos como "PIX", "Campo Grande", "35", "500", "5%".
- **Resiliência e Fallback**: caso o modelo de embeddings ou runtime ONNX não esteja acessível no ambiente, o sistema degrada suavemente para a busca léxica sem interromper o atendimento do assistente.

### Regras de negócio ([src/prompts.py](src/prompts.py))
- Vende exclusivamente instrumentos (sem acessórios, amplificadores, pedais etc.).
- Nunca inventar catálogo, estoque ou status de pedido: sempre usar as ferramentas.
- Dúvidas de frete, troca, devolução, horários e pagamento são tratadas via `search_policies` (políticas da loja em PDF).
- Produto sem estoque ou descontinuado: avisar e sugerir similares.

## Stack
Python, Groq SDK, pandas, PyMuPDF, fastembed (embeddings locais via ONNX), pytest.
