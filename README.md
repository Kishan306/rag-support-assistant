# NovaSaaS Support Chatbot

A full-stack RAG support chatbot for a fictional SaaS product. The backend
is a FastAPI service that answers questions from product documentation using
retrieval-augmented generation (RAG) with Claude. The frontend is a Next.js
chat UI that streams answers token by token.

Built from scratch without high-level frameworks like LangChain, so every
stage of the pipeline (chunking, embedding, retrieval, prompting, streaming)
is explicit and easy to follow.

## Features

- Answers questions grounded in NovaSaaS documentation, with source citations
- Multi-turn conversation memory per session
- Rewrites follow-up questions into standalone search queries, so retrieval
  still works when a question depends on earlier turns (e.g. "what about
  annual plans?" after asking about refunds)
- Streams answers token by token over Server-Sent Events (SSE)
- Detects greetings and small talk in any phrasing and responds without
  running document retrieval
- Refuses out-of-scope questions instead of guessing
- Responsive chat UI for desktop and mobile

## Architecture

Browser (Next.js)
│ POST /chat/stream (SSE)
▼
FastAPI (main.py)
│
├── Smalltalk? (Haiku classifier) → reply directly
│
└── Real question
│
├── Rewrite as standalone query using session history
├── ChromaDB vector search → top chunks above distance threshold
│ (no chunks → canned out-of-scope reply, no LLM call)
└── Claude (Sonnet, streaming) → answer grounded in chunks
│
▼
tokens streamed to the browser, then sources + session_id


## Tech stack

- **Backend:** Python, FastAPI, Server-Sent Events
- **LLM:** Claude (Anthropic SDK). Sonnet for answers, Haiku for smalltalk classification
- **Embeddings:** sentence-transformers `all-MiniLM-L6-v2`, running locally
- **Vector DB:** ChromaDB, persisted to disk
- **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS
- **Containers:** Docker and docker-compose

## Project structure

| Path | Purpose |
|------|---------|
| `docs.py` | Product documentation knowledge base (8 documents) |
| `ingest.py` | Chunks documents, embeds them, and stores them in ChromaDB |
| `query.py` | Retrieval, query rewriting, generation (streaming and non-streaming), smalltalk classification |
| `prompts.py` | Versioned system prompts |
| `main.py` | API endpoints: `/chat`, `/chat/stream`, `/chat/{session_id}/history`, `/health` |
| `session_store.py` | In-memory conversation history per session |
| `eval_embeddings.py` | Retrieval quality evaluation (golden pairs) |
| `eval_rag.py` | Answer quality evaluation (faithfulness, relevance, conciseness) |
| `frontend/` | Next.js chat UI (see `frontend/README.md`) |
| `Dockerfile` | Backend container image |
| `docker-compose.yml` | Runs backend and frontend together |

## Key engineering decisions

**Paragraph-aware chunking with overlap.** Documents are split into roughly
500-character chunks on paragraph boundaries, with 50 characters of overlap
and a minimum-size filter, so that facts crossing a boundary are not lost and
tiny header-only chunks are not stored.

**Distance-threshold filtering.** Chunks farther than a cosine-distance
threshold are discarded before generation. This keeps irrelevant context away
from the model and avoids LLM calls for out-of-scope questions.

**Query rewriting for follow-ups.** Generation naturally uses conversation
history, but vector search does not. Before retrieval, a follow-up question is
rewritten into a standalone query using recent turns. Generation still uses
the user's original wording, so replies stay natural.

**Smalltalk classification instead of keyword lists.** A cheap Haiku call
decides whether a message is small talk or a real question. This handles any
phrasing, including slang, without maintaining a word list.

**Embedding model chosen by measurement.** `bge-small-en-v1.5` has a higher
public benchmark score, but it underperformed `all-MiniLM-L6-v2` on this
project's data in `eval_embeddings.py`, so MiniLM was kept.

**Model tiering.** Sonnet generates answers, and Haiku handles the simple
classification step.

## Setup

### Prerequisites

- Docker and docker-compose (recommended), or Python 3.12 and Node.js 20+
- An Anthropic API key

### Environment

Create a `.env` file in the repo root:

ANTHROPIC_API_KEY=your-key-here


### Option A: Docker (recommended)

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs

### Option B: Run manually

Backend:

```bash
python3 -m venv rag-venv
source rag-venv/bin/activate
pip install -r requirements.txt
python ingest.py            # builds the vector database, run once or after changing docs
uvicorn main:app --reload
```

Frontend (in a separate terminal):

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

The frontend expects the backend at `http://localhost:8000` (set in
`.env.local`). CORS is configured to allow `http://localhost:3000`.

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Single response with `answer`, `sources`, and `session_id` |
| `POST` | `/chat/stream` | Same request, streamed as SSE `token` events followed by a `done` event |
| `GET` | `/chat/{session_id}/history` | Conversation history for a session |
| `GET` | `/health` | Service status and number of indexed chunks |

Example request:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I reset my password?"}'
```

## Evaluation

```bash
python eval_embeddings.py   # retrieval quality: top-1, top-3, document accuracy
python eval_rag.py          # answer quality: faithfulness, relevance, conciseness
```

The golden pairs in `eval_embeddings.py` reference chunk IDs, so they need
updating whenever the documents change.

## Limitations

- Sessions are stored in memory, so they are lost on restart and do not work
  across multiple backend workers.
- No authentication or rate limiting.
- Retrieval is vector-only, with no re-ranking or keyword matching.
- Conversation history is capped at the last 10 messages.
- Answers are capped at 200 tokens, so very broad questions may be truncated.

## What I learned building this

- How RAG grounds an LLM in external documents, and where it fails
- Why retrieval needs its own handling for follow-up questions, separate from generation
- Chunking, distance thresholds, and why embedding models are not interchangeable
- Streaming LLM output to a browser with Server-Sent Events
- Measuring retrieval and answer quality instead of judging by a few examples
- Keeping costs down by matching model size to task complexity

---

Built as part of a structured AI Engineering learning journey.