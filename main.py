# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from query import rag_query, collection, retrieve, generate_stream, contextualize_query, is_smalltalk
from session_store import get_history, append_turn
import uuid
from fastapi.responses import StreamingResponse
import json

app = FastAPI(title="NovaSaaS Support Chatbot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str

class Source(BaseModel):
    id: str
    title: str
    distance: float

class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sources: list[Source]

@app.get("/")
def root():
    return {"status": "ok", "message": "NovaSaaS Support Chatbot is running"}

@app.get("/health")
def health():
    return {"status": "ok", "documents_indexed": collection.count()}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    if len(req.message) > 500:
        raise HTTPException(status_code=400, detail="Message too long, max 500 characters")

    session_id = req.session_id or str(uuid.uuid4())
    history = get_history(session_id)

    result = rag_query(req.message, history=history)

    append_turn(session_id, "user", req.message)
    append_turn(session_id, "assistant", result["answer"])

    return {
        "session_id": session_id,
        "answer": result["answer"],
        "sources": result["sources"]
    }


@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    if len(req.message) > 500:
        raise HTTPException(status_code=400, detail="Message too long, max 500 characters")

    session_id = req.session_id or str(uuid.uuid4())
    history = get_history(session_id)

    def event_stream():
        # Handle greetings/chit-chat before touching retrieval at all
        if is_smalltalk(req.message):
            reply = (
                "Hey! I'm the NovaSaaS support assistant — ask me anything "
                "about billing, your account, or the product."
            )
            yield f"data: {json.dumps({'type': 'token', 'text': reply})}\n\n"
            append_turn(session_id, "user", req.message)
            append_turn(session_id, "assistant", reply)
            yield f"data: {json.dumps({'type': 'done', 'session_id': session_id, 'sources': []})}\n\n"
            return

        search_query = contextualize_query(req.message, history)
        chunks = retrieve(search_query, n_results=5, threshold=0.7)
        
        full_text = ""

        if not chunks:
            fallback = "I don't have information about that in our docs."
            yield f"data: {json.dumps({'type': 'token', 'text': fallback})}\n\n"
            full_text = fallback
            sources = []
        else:
            sources = [{"id": c["id"], "title": c["title"], "distance": round(c["distance"], 4)} for c in chunks]
            for piece in generate_stream(req.message, chunks, history):
                full_text += piece
                yield f"data: {json.dumps({'type': 'token', 'text': piece})}\n\n"

        append_turn(session_id, "user", req.message)
        append_turn(session_id, "assistant", full_text)

        yield f"data: {json.dumps({'type': 'done', 'session_id': session_id, 'sources': sources})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/chat/{session_id}/history")
def chat_history(session_id: str):
    return {"session_id": session_id, "history": get_history(session_id)}