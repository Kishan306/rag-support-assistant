# NovaSaaS RAG Support Assistant

A RAG (Retrieval Augmented Generation) system that answers product 
support questions using ChromaDB for vector search and Claude for generation.

## Setup

1. Clone the repo
2. Create a virtual environment
```bash
   python3 -m venv rag-venv
   source rag-venv/bin/activate
```
3. Install dependencies
```bash
   pip install -r requirements.txt
```
4. Create a `.env` file
ANTHROPIC_API_KEY="your-key-here"

5. Ingest documents into ChromaDB
```bash
   python ingest.py
```
6. Run the API
```bash
   uvicorn main:app --reload
```

## Project Structure

- `docs.py` — product documentation (knowledge base)
- `ingest.py` — embeds docs and stores in ChromaDB (run once)
- `query.py` — RAG pipeline: retrieve → augment → generate
- `main.py` — FastAPI endpoint wrapping the RAG pipeline

## Stack

- Claude (Anthropic) — LLM for answer generation
- ChromaDB — local vector database
- sentence-transformers (all-MiniLM-L6-v2) — embedding model
- FastAPI — API layer