import chromadb
from chromadb.utils import embedding_functions
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()

chroma_client = chromadb.PersistentClient(path=".chromadb")

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

collection = chroma_client.get_collection(
    "novasaas_docs",
    embedding_function=embedding_fn
)

SYSTEM_PROMPT = """You are a helpful support assistant for NovaSaaS.
Answer the user's question using ONLY the context provided below.
If the answer is not in the context, say "I don't have information about that in our docs."
Never make up information. Be concise and direct.
Always mention where the user can find the relevant setting if applicable."""

def retrieve(question: str, n_results: int = 2, threshold: float = 0.6) -> list[dict]:
    """Find the most relevant doc chunks for a question."""
    results = collection.query(
        query_texts=[question],
        n_results=n_results
    )

    retrieved = []

    for i in range(len(results["ids"][0])):
        distance = results["distances"][0][i]
        
        if distance < threshold:
            retrieved.append({
                "id": results["ids"][0][i],
                "title": results["metadatas"][0][i]["title"],
                "content": results["documents"][0][i],
                "distance": results["distances"][0][i]
            })

    return retrieved

def generate(question: str, context_chunks: list[dict]) -> str:
    """Feed retrieved context + question to Claude and get an answer."""

    context = "\n\n---\n\n".join([
        f"[{chunk['title']}]\n{chunk['content']}"
        for chunk in context_chunks
    ])

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Context from our documentation:\n\n{context}\n\nQuestion: {question}"
            }
        ]
    )

    return message.content[0].text


def rag_query(question: str) -> dict:
    """Full RAG pipeline: retrieve -> augment -> generate."""

    chunks = retrieve(question, n_results=2)

    if not chunks:
        return {
            "question": question,
            "answer": "I don't have information about that in our docs.",
            "sources": []
        }

    answer = generate(question, chunks)

    return {
        "question": question,
        "answer": answer,
        "sources": [{"id": c["id"], "title": c["title"], "distance": round(c["distance"], 4)} for c in chunks]
    }


if __name__ == "__main__":
    questions = [
        # "How do I reset my password?",
        # "What is the refund policy?",
        "Can I use the API on a free plan?",
        "How do I add someone to my team?",
        "What is the weather in Mumbai?"
    ]

    for question in questions:
        print(f"\nQ: {question}")
        result = rag_query(question)
        print(f"A: {result['answer']}")
        print(f"Sources: {[s['title'] for s in result['sources']]}")
        print("-"*60)