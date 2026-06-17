# NovaSaaS AI Support Assistant

An AI-powered customer support system for a fictional SaaS product, built from
scratch without high-level frameworks like LangChain. Combines Retrieval-Augmented
Generation (RAG), an agentic tool-use loop, and production-grade error handling.

Built as a hands-on AI Engineering project covering the full stack — from raw
LLM calls to a multi-tool autonomous agent.

## What it does

Answers customer support questions by intelligently choosing between:
- **Searching product documentation** (RAG over a vector database)
- **Looking up specific user accounts** (database tool)
- **Performing calculations** (calculator tool)
- **Answering directly** when no tool is needed

The agent decides per-question which tools to use, and can chain multiple tools
together — for example, looking up a user's project count and then running a
calculation on it.

## Architecture
User question

│

▼

Agent (Claude) ── decides which tool(s) to use

│

├── search_docs    → ChromaDB vector search → relevant doc chunks

├── lookup_account → account database

└── calculator     → arithmetic

│

▼

Final answer (grounded in tool results)

## Tech stack

- **LLM:** Claude (Anthropic) via the official SDK
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2), running locally
- **Vector DB:** ChromaDB (persistent, local)
- **API layer:** FastAPI
- **Evaluation:** custom retrieval + LLM-as-judge evaluation suites

## Project structure

| File | Purpose |
|------|---------|
| `docs.py` | Product documentation (knowledge base) |
| `ingest.py` | Chunks documents, embeds them, stores in ChromaDB |
| `query.py` | RAG pipeline: retrieve → augment → generate, with cost tracking |
| `prompts.py` | Versioned system prompts |
| `main.py` | FastAPI endpoints for the RAG system |
| `agent.py` | Minimal agent demonstrating the tool-use loop |
| `rag_agent.py` | Agent combining RAG, account, and calculator tools |
| `rag_agent_prod.py` | Production-hardened version: error handling, iteration limits, logging |
| `eval_embeddings.py` | Retrieval quality evaluation |
| `eval_rag.py` | Answer quality evaluation (faithfulness, relevance, conciseness) |

## Key engineering decisions

**Custom chunking with overlap.** Documents are split into ~500-character
paragraph-aware chunks with 50-character overlap and a minimum-size filter,
rather than naive fixed-size splitting, to preserve semantic coherence.

**Distance-threshold filtering.** Retrieved chunks below a similarity threshold
are discarded before reaching the LLM — preventing hallucination from irrelevant
context and avoiding unnecessary API calls for out-of-scope questions.

**Evaluation-driven development.** Both retrieval and answer quality are measured
with dedicated eval suites. Embedding model choice was validated empirically: a
higher-benchmark model (bge-small-en-v1.5) was tested and rejected after it
underperformed all-MiniLM-L6-v2 on this specific dataset — a reminder that public
benchmarks don't always predict performance on your own data.

**Model tiering for cost.** Uses Claude Sonnet rather than Opus for the RAG
generation step — roughly 6x cheaper per query with no measurable quality loss
for this use case.

**Production-hardened agent loop.** The agent enforces a maximum iteration limit
(preventing infinite loops), wraps every tool call in error handling (one tool
failing degrades gracefully instead of crashing the request), and logs every
step to file for observability.

## Setup

1. Clone the repo
```bash
   git clone git@github.com:Kishan306/rag-support-assistant.git
   cd rag-support-assistant
```

2. Create and activate a virtual environment
```bash
   python3 -m venv rag-venv
   source rag-venv/bin/activate
```

3. Install dependencies
```bash
   pip install -r requirements.txt
```

4. Create a `.env` file with your API key
ANTHROPIC_API_KEY=your-key-here

5. Build the vector database (run once)
```bash
   python ingest.py
```

## Usage

**Run the RAG API:**
```bash
uvicorn main:app --reload
# then visit http://localhost:8000/docs
```

**Run the agent:**
```bash
python rag_agent_prod.py
```

**Run evaluations:**
```bash
python eval_embeddings.py   # retrieval quality
python eval_rag.py          # answer quality
```

## What I learned building this

- How LLMs work at the token and embedding level, and how RAG grounds them in
  external knowledge
- Vector search mechanics: cosine similarity, distance thresholds, and why
  embedding models are not interchangeable
- Prompt engineering patterns for reliable, structured LLM output
- Evaluating AI systems rigorously rather than eyeballing a few examples
- Building agents from scratch: tool definitions, the agentic loop, and
  multi-tool orchestration
- Production concerns: cost management, error handling, iteration limits, and
  observability

---

Built as part of a structured AI Engineering learning journey.