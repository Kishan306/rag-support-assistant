import chromadb
from chromadb.utils import embedding_functions
import anthropic
from dotenv import load_dotenv
from prompts import ACTIVE_RAG_PROMPT
import time

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

def retrieve(question: str, n_results: int = 3, threshold: float = 0.6) -> list[dict]:
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


def generate(question: str, context_chunks: list[dict], history: list[dict] = None) -> tuple[str, dict]:
    """Feed retrieved context + question (+ prior turns) to Claude and get an answer."""

    context = "\n\n---\n\n".join([
        f"[{chunk['title']}]\n{chunk['content']}"
        for chunk in context_chunks
    ])

    # Start with prior conversation turns, if any
    messages = list(history) if history else []

    # Append the current turn with fresh retrieved context
    messages.append({
        "role": "user",
        "content": f"Documentation:\n\n{context}\n\nQuestion: '''{question}'''"
    })

    start = time.time()

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        temperature=0.3,
        system=ACTIVE_RAG_PROMPT,
        messages=messages
    )

    latency = time.time() - start

    input_tokens = message.usage.input_tokens
    output_tokens = message.usage.output_tokens

    input_cost = input_tokens / 1000000 * 3.00
    output_cost = output_tokens / 1000000 * 15.00
    total_cost = input_cost + output_cost

    cost_meta = {
        "model": "claude-sonnet-4-6",
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": round(total_cost, 8),
        "latency_sec": round(latency, 2)
    }

    return message.content[0].text, cost_meta


def rag_query(question: str, history: list[dict] = None) -> dict:
    """Full RAG pipeline: retrieve -> augment -> generate. Optionally multi-turn."""

    if is_smalltalk(question):
        return {
            "question": question,
            "answer": (
                "Hey! I'm the NovaSaaS support assistant — ask me anything "
                "about billing, your account, or the product."
            ),
            "sources": [],
            "cost": None
        }

    search_query = contextualize_query(question, history)
    chunks = retrieve(search_query, n_results=5, threshold=0.7)

    if not chunks:
        return {
            "question": question,
            "answer": "I don't have information about that in our docs.",
            "sources": [],
            "cost": None
        }

    answer, cost_meta = generate(question, chunks, history)

    return {
        "question": question,
        "answer": answer,
        "sources": [{"id": c["id"], "title": c["title"], "distance": round(c["distance"], 4)} for c in chunks],
        "cost": cost_meta
    }


def is_smalltalk(message: str) -> bool:
    """Cheap classification: is this a greeting/chit-chat, or a real question?
    Uses Haiku since this is a simple binary decision — no need for a bigger model."""
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=5,
        temperature=0,
        system=(
            "Classify the message. Reply with only one word: SMALLTALK or QUESTION. "
            "SMALLTALK = greetings, thanks, goodbyes, casual chat, slang greetings, "
            "emoji-only messages, or anything with no real question in it. "
            "QUESTION = anything asking about a product, account, billing, or seeking real information."
        ),
        messages=[{"role": "user", "content": message}]
    )
    return response.content[0].text.strip().upper() == "SMALLTALK"


def generate_stream(question: str, context_chunks: list[dict], history: list[dict] = None):
    """Yields answer text in pieces as Claude generates them."""
    context = "\n\n---\n\n".join([
        f"[{chunk['title']}]\n{chunk['content']}"
        for chunk in context_chunks
    ])

    messages = list(history) if history else []
    messages.append({
        "role": "user",
        "content": f"Documentation:\n\n{context}\n\nQuestion: '''{question}'''"
    })

    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=200,
        temperature=0.3,
        system=ACTIVE_RAG_PROMPT,
        messages=messages
    ) as stream:
        print(f"[DEBUG] Full messages sent: {messages}")
        for text in stream.text_stream:
            yield text


def contextualize_query(question: str, history: list[dict]) -> str:
    """Rewrites a follow-up question into a standalone query using recent history,
    so retrieval has enough context to find the right chunks."""
    if not history:
        return question

    recent = history[-4:]  # last couple of turns is enough
    history_text = "\n".join([f"{h['role']}: {h['content']}" for h in recent])

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=60,
        temperature=0,
        system="Rewrite the follow-up question as a standalone question using the conversation. Reply with ONLY the rewritten question, nothing else.",
        messages=[{
            "role": "user",
            "content": f"Conversation:\n{history_text}\n\nFollow-up question: {question}\n\nStandalone question:"
        }]
    )
    return response.content[0].text.strip()


if __name__ == "__main__":
    questions = [
        "How do I reset my password?",
        "What is the refund policy?",
        "Can I use the API on a free plan?",
        "How do I add someone to my team?",
        "What is the weather in Mumbai?"
    ]

    for question in questions:
        print(f"\nQ: {question}")
        result = rag_query(question)
        print(f"A: {result['answer']}")
        print(f"Sources: {[s['title'] for s in result['sources']]}")
        if result['cost']:
            print(f"Cost metadata: {result['cost']}")
        else:
            print(f"Cost metadata: no API call made (out of scope)")
        print("-" * 60)