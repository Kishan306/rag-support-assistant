from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from query import rag_query, collection

app = FastAPI(
    title="NovaSaaS Support Assistant",
    description="RAG-powered support assistant for NovaSaaS documentation",
    version="1.0.0"
)

class QuestionRequest(BaseModel):
    question: str

class Source(BaseModel):
    id: str
    title: str
    distance: float

class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[Source]

@app.get("/")
def root():
    return {"status": "ok", "message": "NovaSaaS Support Assistant is running"}

@app.post("/ask", response_model=QuestionResponse)
def ask(req: QuestionRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if len(req.question) > 500:
        raise HTTPException(status_code=400, detail="Question cannot be longer than 500 characters")

    result = rag_query(req.question)
    return result

@app.get("/health")
def health():
    count = collection.count()
    return {"status": "ok", "collection_indexed": count}