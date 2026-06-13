import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from docs import DOCS

load_dotenv()

chroma_client = chromadb.PersistentClient(path=".chromadb")

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name = "BAAI/bge-small-en-v1.5"
)

try:
    chroma_client.delete_collection("novasaas_docs")
except:
    pass

collection = chroma_client.create_collection("novasaas_docs", embedding_function=embedding_fn)

def paragraph_chunks(text: str, max_chars: int = 500, overlap: int = 50, min_chars: int = 100) -> list[str]:
    """Split text into overlapping paragraph-aware chunks."""
    # Split on double newline or single newline
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks = []
    current = ""

    for para in paragraphs:
        if not current:
            current = para
        elif len(current) + len(para) + 2 <= max_chars:
            current = current + "\n\n" + para
        else:
            if len(current) >= min_chars:
                chunks.append(current)
            # overlap: carry last N chars of current into next chunk
            overlap_text = current[-overlap:] if len(current) > overlap else current
            current = overlap_text + "\n\n" + para

    if current:
        chunks.append(current)

    # Safety check — ensure every chunk is a string
    return [str(c) for c in chunks]

def ingest_docs():
    print(f"Ingesting {len(DOCS)} documents with chunking...")

    total_chunks = 0

    for doc in DOCS:
        chunks = paragraph_chunks(doc["content"], max_chars=500, overlap=50)

        print(f"   [{doc['id']}] {doc['title']} -> {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc['id']}-chunk-{i}"

            collection.add(
                ids=[chunk_id],
                documents=[chunk],
                metadatas=[{
                    "title": doc["title"],
                    "doc_id": doc["id"],
                    "chunk_index": i,
                    "chunk_total": len(chunks),
                    "char_count": len(chunk)
                }]
            )
            total_chunks += 1

    print(f"\n Done. {total_chunks} chunks stored across {len(DOCS)} documents")

if __name__ == "__main__":
    ingest_docs()