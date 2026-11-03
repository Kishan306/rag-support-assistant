# NovaSaaS AI Support Assistant

A full-stack AI-powered customer support system for a fictional SaaS product,
built from scratch without high-level frameworks like LangChain. Combines
Retrieval-Augmented Generation (RAG), an agentic tool-use loop, a streaming
multi-turn chatbot, and a Next.js frontend — with production-grade error
handling throughout.

Built as a hands-on AI Engineering project covering the full stack — from raw
LLM calls to a multi-tool autonomous agent to a deployable full-stack chatbot.

## What it does

Two ways to interact with the system:

**Chatbot (primary interface)** — a conversational support assistant with a
Next.js chat UI. It:
- Answers questions grounded in NovaSaaS documentation via RAG
- Maintains multi-turn conversation memory per session
- Rewrites follow-up questions into standalone search queries so retrieval
  still works correctly across a conversation (e.g. "what about annual
  plans?" after asking about refunds)
- Streams answers token by token instead of waiting for the full response
- Detects greetings and small talk (in any phrasing, including slang) and
  responds naturally instead of forcing them through document retrieval
- Cites which documentation sections an answer came from

**Agent (tool-use demo)** — a separate, tool-calling agent that intelligently
chooses between:
- Searching product documentation (RAG over a vector database)
- Looking up specific user accounts (database tool)
- Performing calculations (calculator tool)
- Answering directly when no tool is needed

The agent can chain multiple tools together — for example, looking up a
user's project count and then running a calculation on it.

## Architecture

**Chatbot flow:**

User message (Next.js frontend)
│
▼
POST /chat/stream (FastAPI, SSE)
│
├── Smalltalk? → respond directly, skip retrieval
│
└── Real question:
│
▼
Rewrite as standalone query using session history
│
▼
ChromaDB vector search → relevant doc chunks (threshold-filtered)
│
▼
Claude (streaming) → answer grounded in chunks + conversation history
│
▼
Tokens streamed to frontend as they generate


**Agent flow (separate demo):**

User question
│
▼
Agent (Claude) ── decides which tool(s) to use
│
├── search_docs → ChromaDB vector search → relevant doc chunks
├── lookup_account → account database
└── calculator → arithmetic
│
▼
Final answer (grounded in tool results)


## Tech stack

- **LLM:** Claude (Anthropic) via the official SDK — Sonnet for generation,
  Haiku for cheap smalltalk classification
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2), running locally
- **Vector DB:** ChromaDB (persistent, local)
- **Backend:** FastAPI, with Server-Sent Events (SSE) for streaming
- **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS
- **Evaluation:** custom retrieval + LLM-as-judge evaluation suites
- **Containerization:** Docker + docker-compose (one-command startup for both
  services)

## Project structure

| Path | Purpose |
|------|---------|
| `docs.py` | Product documentation knowledge base (8 documents: billing, account, technical, getting started, task features, notifications, mobile/offline, support) |
| `ingest.py` | Chunks documents, embeds them, stores in ChromaDB |
| `query.py` | RAG pipeline: query rewriting, retrieve, augment, generate (streaming + non-streaming), cost tracking, smalltalk classification |
| `prompts.py` | Versioned system prompts |
| `main.py` | FastAPI endpoints — `/chat`, `/chat/stream`, `/health` |
| `session_store.py` | In-memory per-session conversation history |
| `agent.py` | Minimal agent demonstrating the tool-use loop |
| `rag_agent.py` | Agent combining RAG, account, and calculator tools |
| `rag_agent_prod.py` | Production-hardened agent: error handling, iteration limits, logging |
| `eval_embeddings.py` | Retrieval quality evaluation |
| `eval_rag.py` | Answer quality evaluation (faithfulness, relevance, conciseness) |
| `frontend/` | Next.js chat UI (see `frontend/README.md`) |
| `Dockerfile` | Backend container image |
| `docker-compose.yml` | Runs backend + frontend together |

## Key engineering decisions

**Custom chunking with overlap.** Documents are split into ~500-character
paragraph-aware chunks with 50-character overlap and a minimum-size filter,
rather than naive fixed-size splitting, to preserve semantic coherence.

**Distance-threshold filtering.** Retrieved chunks below a similarity
threshold are discarded before reaching the LLM — preventing hallucination
from irrelevant context and avoiding unnecessary API calls for out-of-scope
questions.

**Conversational query rewriting.** A follow-up question like "what about
annual plans?" is semantically meaningless to a vector search on its own.
Before retrieval, the current question is rewritten into a standalone query
using recent conversation history, so search finds the right chunks even
when the user's phrasing depends on earlier context. Generation still uses
the user's original wording, so responses stay natural.

**Smalltalk short-circuiting.** Greetings and casual chat are classified by
a cheap Haiku call before retrieval runs, rather than matched against a fixed
keyword list — this correctly handles arbitrary phrasing (including slang)
without ever needing to guess and maintain a word list.

**Evaluation-driven development.** Both retrieval and answer quality are
measured with dedicated eval suites. Embedding model choice was validated
empirically: a higher-benchmark model (bge-small-en-v1.5) was tested and
rejected after it underperformed all-MiniLM-L6-v2 on this specific dataset —
a reminder that public benchmarks don't always predict performance on your
own data.

**Model tiering for cost.** Uses Claude Sonnet for RAG generation (roughly
6x cheaper than Opus with no measurable quality loss here) and Haiku for the
trivial smalltalk classification step — matching model cost to task
complexity throughout.

**Production-hardened agent loop.** The agent enforces a maximum iteration
limit (preventing infinite loops), wraps every tool call in error handling
(one tool failing degrades gracefully instead of crashing the request), and
logs every step to file for observability.

## Setup

1. Clone the repo
```bash
   git clone git@github.com:Kishan306/rag-support-assistant.git
   cd rag-support-assistant
```

2. Create a `.env` file with your API key

ANTHROPIC_API_KEY=your-key-here


### Option A — Run everything with Docker (recommended)

```bash
docker-compose up --build
```
- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/docs

### Option B — Run manually (backend)

```bash
python3 -m venv rag-venv
source rag-venv/bin/activate
pip install -r requirements.txt
python ingest.py          # build the vector database, run once
uvicorn main:app --reload
```

### Option B — Run manually (frontend)

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```
See `frontend/README.md` for more detail on the frontend specifically.

## Usage

**Chat via the UI:** open http://localhost:3000 and start typing.

**Chat via the API directly:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I reset my password?"}'
```

**Run the tool-use agent (separate from the chatbot):**
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
- That retrieval and generation have different context needs — generation
  benefits from full conversation history for free, but retrieval needs an
  explicit query-rewriting step to use that same history effectively
- Turning a backend-only RAG pipeline into a real chatbot: sessions,
  streaming, and graceful handling of small talk
- Production concerns: cost management, error handling, iteration limits,
  and observability

---

Built as part of a structured AI Engineering learning journey.