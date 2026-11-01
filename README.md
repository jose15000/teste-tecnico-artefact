# Teste Técnico Artefact — Atendente Virtual da Empório da Música

Agente de atendimento conversacional (estilo WhatsApp) para a **Empório da Música**, loja de instrumentos musicais em Campo Grande/MS. O assistente utiliza LLM via **Groq** com *function/tool calling* nativo sobre bases relacionais da loja (CSVs) e um pipeline RAG híbrido sobre o manual de políticas internas (PDF).

---

## Como Executar

### 1. Pré-requisitos e Ambiente
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # configure sua chave GROQ_API_KEY
```

### 2. Iniciar Atendimento (CLI)
```bash
python main.py
```
- Comandos úteis no terminal: `sair` encerra o atendimento, `limpar` reinicia a conversa.

### 3. Rodar Testes Automatizados
```bash
pytest
```

---

## Configuração (`.env`)

A única variável obrigatória é a chave da API da Groq:

| Variável | Descrição | Obrigatória |
|---|---|:---:|
| `GROQ_API_KEY` | Chave da API da Groq | Sim |

> **Nota:** O modelo da Groq (`openai/gpt-oss-120b`) e o modelo de embeddings (`sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`) já possuem valores padrão configurados diretamente no código, não sendo necessário defini-los no `.env`. Caso deseje sobrescrevê-los para testes, você pode opcionalmente definir `GROQ_MODEL` e `EMBEDDING_MODEL`.

---

## Arquitetura do Projeto

```
main.py                CLI interativa de atendimento
src/
├── agent.py           Loop ReAct de tool calling com tolerância a falhas
├── prompts.py         System prompt com persona e diretrizes de negócio
├── tools.py           Ferramentas: search_products, get_order_status, search_policies
├── tools_schema.py    Schemas JSON de ferramentas em conformidade com o LLM
├── data_loader.py     Carga, normalização e indexação em memória dos CSVs
└── rag.py             Engine de busca híbrida (vetorial + léxica) no PDF de políticas
data/                  Bases CSVs da loja e políticas_da_loja.pdf
conversations/         Transcrições completas de 4 cenários de teste reais
tests/                 Suíte de testes automatizados com pytest
```

---

## Justificativa das Decisões Técnicas

### 1. Framework / Abordagem do Agente
- **Tool Calling Nativo em Loop ReAct Direto (sem LangChain / CrewAI):** Optou-se por construir o agente em Python puro utilizando o SDK oficial da Groq.
- **Racional:** Frameworks orquestradores pesados introduzem camadas excessivas de abstração, sobrecarga de dependências, menor determinismo e dificultam a depuração fina de mensagens malformadas. O loop em `src/agent.py` oferece controle absoluto sobre o histórico, tratamento granular de exceções (como `output_parse_failed` e `tool_use_failed`) e retorno de erros diretamente como contexto (`role: tool`) para auto-recuperação do modelo.

### 2. Provedor e Modelo (LLM)
- **Groq com `openai/gpt-oss-120b`:**
- **Racional:** Em um canal de atendimento conversacional (estilo WhatsApp), a latência da primeira resposta é crucial para uma boa experiência do cliente. Os chips LPU da Groq entregam centenas de tokens por segundo com tempo de resposta quase instantâneo, aliado a um suporte robusto a *function calling* e excelente capacidade de interpretação em português.

### 3. Arquitetura de Retrieval (RAG)
- **Extração Estruturada e Chunking Hierárquico:** O texto do PDF é extraído via `PyMuPDF` limpando cabeçalhos e rodapés repetitivos, sendo segmentado hierarquicamente pelas seções numeradas (1 a 10 e subitens como 5.1, 5.2). Cada trecho herda o título da seção pai (ex.: `5. Política de Frete e Entregas — 5.1 Entregas na Região Metropolitana de Campo Grande`), garantindo contexto semântico completo aos chunks.
- **Busca Híbrida (Densa + Léxica):**
  - *Densa:* Embeddings multilingues gerados localmente via `fastembed` em runtime ONNX sem necessidade de PyTorch ou GPU.
  - *Léxica:* Bônus ponderado em títulos e conteúdo para palavras-chave exatas, garantindo precisão cirúrgica em valores críticos (ex.: `"PIX"`, `"5%"`, `"Campo Grande"`, `"R$ 35"`, `"500"`).
- **100% em Memória RAM (Singleton Lazy-Loading):** Todo o índice vetorial e léxico é computado uma única vez na inicialização e mantido em memória via `numpy.dot`, sem dependência de bancos de vetores externos (Pinecone, Chroma, Qdrant).
- **Degradação Segura (Fallback):** Caso o modelo ONNX não esteja disponível no ambiente, o mecanismo degrada automaticamente para a busca léxica sem interromper a execução do assistente.

### 4. Estratégia de Prompt e Persona
- **Persona:** Atendente atencioso, conhecedor de música, ágil e focado na realidade local da loja em Campo Grande/MS.
- **Diretrizes Estritas:**
  1. *Exclusividade de Instrumentos:* A loja não vende acessórios avulsos (cordas avulsas, palhetas, cabos, pedais, amplificadores); o atendente recusa com simpatia e redireciona para instrumentos.
  2. *Anti-Alucinação:* Proibição de inventar estoques, preços ou status de pedidos sem invocar as ferramentas correspondentes.
  3. *Consulta Obrigatória a Políticas:* Regras de frete, prazos, trocas, devoluções, garantia, horários e formas de pagamento devem sempre ser checadas via `search_policies`.
  4. *Gestão de Ruptura:* Se um produto procurado estiver esgotado, avisar com clareza e recomendar modelos similares ativos em estoque.
  5. *Foco no Escopo:* Perguntas totalmente alheias à loja ou a instrumentos são tratadas com cordialidade, esclarecendo o propósito da Empório da Música.

### 5. Tratamento de Dados e Privacidade
- **Validação de Identidade em Pedidos:** A ferramenta `get_order_status` exige tanto o número do pedido quanto o telefone do cliente. Se o telefone não coincidir com o cadastro, a API retorna mensagem genérica de não encontrado, impedindo enumeração e vazamento de pedidos por terceiros.
- **Normalização e Flexibilidade Gramatical:** Funções de normalização Unicode (`normalize_text`) removem diacríticos e tratam singular/plural de categorias (ex.: a busca por `"violão"` casa com a categoria `"Violões"`).

---

## Exemplos de Interação Registrados

O repositório conta com 4 transcrições reais de conversas executadas contra o modelo Groq na pasta [`conversations/`](conversations/):

| Arquivo | Cenário Coberto | Destaques |
|---|---|---|
| [`01_catalogo_e_precos.md`](conversations/01_catalogo_e_precos.md) | Consulta de Catálogo e Preços | Filtro de violões até R$ 1.000, ordenação por preço e consulta detalhada do Takamine GD20. |
| [`02_politicas_e_devolucoes.md`](conversations/02_politicas_e_devolucoes.md) | Informações Gerais e Políticas | Consulta de endereço/horários no centro de Campo Grande e direito de arrependimento (7 dias, frete reverso grátis). |
| [`03_status_de_pedido_e_rastreio.md`](conversations/03_status_de_pedido_e_rastreio.md) | Status de Pedido e Rastreamento | Exigência segura de telefone antes da consulta e emissão do código de rastreio `BRJL5544332BR`. |
| [`04_casos_de_borda_e_fora_de_escopo.md`](conversations/04_casos_de_borda_e_fora_de_escopo.md) | Casos de Borda e Fora de Escopo | Produto sem estoque com sugestão de Sunburst alternativo, recusa educada de palhetas e recusa cordial de conserto de micro-ondas. |

---

## Limitações Conhecidas e Próximos Passos (Mais Tempo)

1. **Persistência de Sessões em Banco de Dados:** Atualmente o histórico reside na memória da sessão CLI. Com mais tempo, integraria persistência durável via PostgreSQL ou Redis com TTL para suportar milhares de sessões concorrentes de clientes.
2. **Integração com Mensageria Real:** Conexão direta com a WhatsApp Cloud API (ou provedores como Twilio/Z-API) via webhooks assíncronos.
3. **Re-ranking Neural para RAG:** Adição de um modelo cross-encoder (ex.: `bge-reranker-base`) após o estágio de recuperação híbrida, aumentando ainda mais a precisão em perguntas com múltiplas cláusulas de políticas.
4. **Cache em Disco de Embeddings do PDF:** Serializar os vetores calculados do PDF em arquivo binário (`.npy` ou `.parquet`), reduzindo o tempo de inicialização a zero em qualquer ambiente.
5. **Checkout Interativo com PIX Copia-e-Cola:** Criação de tool para gerar payload de PIX dinâmico com reserva de estoque temporária (15 minutos).

---

## Uso de Assistentes de Código

No desenvolvimento deste projeto, utilizei o **Antigravity (agente inteligente de engenharia de software)** como acelerador de desenvolvimento. 

### Como foi utilizado no workflow:
- **Scaffolding e Estrutura Inicial:** Agilização na criação de boilerplate, schemas JSON de ferramentas e arquivos de configuração.
- **Elaboração de Expressões Regulares e Chunking:** Apoio na estruturação do parser hierárquico do PDF no `src/rag.py` para detecção de seções e subseções.
- **Diagnóstico de Schemas e Robustez:** Identificação rápida de restrições do validador de schemas da Groq (como parâmetros opcionais gerando erro 400 ao receber `null`, corrigidos com `anyOf: [..., null]`).
- **Automação de Testes e Cenários:** Auxílio na escrita da suíte de 14 testes unitários automatizados com `pytest` e na gravação automatizada dos diálogos na pasta `conversations/`.
