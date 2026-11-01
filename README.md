# Artefact Technical Challenge — Empório da Música Virtual Agent

A conversational customer service agent (WhatsApp style) for **Empório da Música**, a musical instrument retail store based in Campo Grande/MS, Brazil. The assistant leverages an LLM via **Groq** with native *function/tool calling* over relational store datasets (CSVs) and a hybrid RAG pipeline over the internal customer service policy manual (PDF).

---

## How to Run

### 1. Prerequisites and Setup
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your GROQ_API_KEY
```

### 2. Start Customer Service Chat (CLI)
```bash
python main.py
```
- Available commands in chat: `sair` (or `exit`/`quit`) terminates the session, `limpar` resets conversation history.

### 3. Run Automated Tests
```bash
pytest
```

---

## Configuration (`.env`)

The only required environment variable is the Groq API key:

| Variable | Description | Required |
|---|---|:---:|
| `GROQ_API_KEY` | Groq API Key | Yes |

> **Note:** Both the LLM (`openai/gpt-oss-120b`) and the local embedding model (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`) have built-in default values defined directly in the code, so defining them in `.env` is entirely optional. If you wish to override them for testing, you may set `GROQ_MODEL` and `EMBEDDING_MODEL`.

---

## Project Architecture

```
main.py                Interactive CLI entry point
src/
├── agent.py           ReAct tool calling loop with retry mechanisms
├── prompts.py         System prompt, persona, and core business guidelines
├── tools.py           Tools: search_products, get_order_status, search_policies
├── tools_schema.py    JSON function schemas matching LLM specifications
├── data_loader.py     Data loading, normalization, and in-memory indexing of CSVs
└── rag.py             Hybrid search engine (dense vector + lexical) over policies PDF
data/                  CSV databases and políticas_da_loja.pdf
conversations/         Transcripts of 4 real test scenarios executed against the model
tests/                 Automated test suite with pytest
```

---

## Justification of Technical Decisions

### 1. Agent Framework and Approach
- **Native Tool Calling with Direct ReAct Loop (No LangChain / CrewAI):** The agent is built in pure Python using the official Groq SDK.
- **Rationale:** Heavy orchestration frameworks introduce unnecessary layers of abstraction, dependency bloat, reduced determinism, and make fine-grained debugging of malformed tool calls difficult. The lightweight loop in `src/agent.py` provides total control over message history, granular exception handling (such as `output_parse_failed` and `tool_use_failed`), and returns tool execution errors directly as context (`role: tool`) so the model can self-correct.

### 2. LLM Provider and Model
- **Groq with `openai/gpt-oss-120b`:**
- **Rationale:** In a conversational messaging channel (WhatsApp style), time-to-first-token is critical for user experience. Groq's LPU architecture delivers hundreds of tokens per second with near-instantaneous responses, combined with robust native function calling and strong comprehension of Portuguese.

### 3. Retrieval Architecture (RAG)
- **Structured Extraction and Hierarchical Chunking:** PDF text is extracted using `PyMuPDF`, filtering out repetitive headers and footers, and hierarchically segmented by numbered sections (1 to 10 and subitems like 5.1, 5.2). Each chunk retains its parent section title (e.g., `5. Política de Frete e Entregas — 5.1 Entregas na Região Metropolitana de Campo Grande`), preserving complete semantic context.
- **Hybrid Search (Dense + Lexical):**
  - *Dense:* Multilingual embeddings generated locally via `fastembed` in ONNX Runtime without requiring PyTorch or GPU acceleration.
  - *Lexical:* Weighted bonuses applied to titles and contents for exact keyword matches, guaranteeing precision for critical terms (e.g., `"PIX"`, `"5%"`, `"Campo Grande"`, `"R$ 35"`, `"500"`).
- **100% In-Memory RAM (Singleton Lazy-Loading):** The entire vector and lexical index is computed once upon initialization and evaluated in memory via `numpy.dot`, eliminating dependencies on external vector databases (Pinecone, Chroma, Qdrant).
- **Graceful Fallback:** If the ONNX model is unavailable in the environment, the retrieval engine degrades smoothly to lexical search without interrupting customer service.

### 4. Prompt Engineering and Persona Strategy
- **Persona:** Cordial, professional, knowledgeable about music, agile, and aligned with local retail in Campo Grande/MS.
- **Strict Guidelines:**
  1. *Instruments Exclusivity:* The store does not sell accessories (spare strings, picks, cables, pedals, amplifiers); the agent politely declines and guides the user toward instruments.
  2. *Anti-Hallucination:* Prohibits fabricating inventory, prices, or order statuses without invoking the respective tools.
  3. *Mandatory Policy Lookups:* Freight costs, delivery timeframes, exchanges, returns, warranties, store hours, and payment terms must always be checked via `search_policies`.
  4. *Stockout Handling:* When a requested item is out of stock, the agent is transparent and suggests active similar alternatives in stock.
  5. *Scope Control:* Out-of-scope inquiries (e.g., electronics repair, general knowledge) are politely declined while redirecting the user back to the store's instruments.

### 5. Data Processing and Privacy Safeguards
- **Identity Verification for Orders:** The `get_order_status` tool requires both the order ID and the customer's registered phone number. If the phone does not match, a generic not-found message is returned to prevent order enumeration and unauthorized data exposure.
- **Normalization and Grammatical Flexibility:** Unicode normalization (`normalize_text`) strips accents and handles singular/plural category inflections in Portuguese (e.g., searching for `"violão"` correctly matches the `"Violões"` category).

---

## Recorded Interaction Examples

The repository includes 4 real conversation transcripts executed against the Groq model in the [`conversations/`](conversations/) directory:

| File | Scenario Covered | Key Highlights |
|---|---|---|
| [`01_catalogo_e_precos.md`](conversations/01_catalogo_e_precos.md) | Catalog & Price Inquiry | Filter acoustic guitars under R$ 1,000, price sorting, and detailed specs inquiry for the Takamine GD20. |
| [`02_politicas_e_devolucoes.md`](conversations/02_politicas_e_devolucoes.md) | Store Info & Policies | Store address and working hours in downtown Campo Grande, and right of withdrawal policy (7 days, free reverse logistics). |
| [`03_status_de_pedido_e_rastreio.md`](conversations/03_status_de_pedido_e_rastreio.md) | Order Status & Tracking | Secure phone verification before revealing order details, and returning tracking code `BRJL5544332BR`. |
| [`04_casos_de_borda_e_fora_de_escopo.md`](conversations/04_casos_de_borda_e_fora_de_escopo.md) | Edge Cases & Out-of-Scope | Out-of-stock item with Sunburst alternative suggestions, polite refusal of picks, and courteous decline of microwave repairs. |

---

## Known Limitations and Next Steps (Given More Time)

1. **Persistent Session Storage:** Conversation history is currently stored in memory during the interactive CLI session. Given more time, durable persistence via PostgreSQL or Redis with TTL would be added to support concurrent sessions across users.
2. **Real Messaging Channel Integration:** Direct integration with the WhatsApp Cloud API (or Twilio/Z-API) through asynchronous webhooks.
3. **Neural Re-Ranking for RAG:** Implementing a cross-encoder model (e.g., `bge-reranker-base`) following the hybrid retrieval phase to further refine ranking on complex multi-clause inquiries.
4. **Disk Cache for PDF Embeddings:** Serializing the computed vector matrices to disk (`.npy` or `.parquet`) to eliminate initialization time across cold starts.
5. **Interactive Checkout with Instant PIX:** A tool to generate dynamic PIX copy-and-paste payment codes with a temporary 15-minute stock hold.

---

## Use of AI Coding Assistants

During the development of this project, I used **Antigravity (an advanced AI software engineering agent)** as a development accelerator.

### How it was used in the workflow:
- **Scaffolding and Setup:** Accelerating boilerplate generation, JSON tool schemas, and environment configuration.
- **Regex & Chunking Refinement:** Structuring the hierarchical PDF parser in `src/rag.py` to identify main sections and subsections accurately.
- **Schema Validation & Robustness:** Diagnosing strict Groq schema validation constraints (e.g., handling optional parameters by allowing `anyOf: [..., null]` to prevent 400 errors).
- **Test Automation & Scenario Recording:** Assisting in writing the 14-test suite with `pytest` and automating the recording of realistic conversation dialogues in `conversations/`.
