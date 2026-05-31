import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
from docs import DOCS

load_dotenv()

chroma_client = chromadb.PersistentClient(path=".chromadb")

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name = "all-MiniLM-L6-v2"
)

try:
    chroma_client.delete_collection("novasaas_docs")
except:
    pass

collection = chroma_client.create_collection("novasaas_docs", embedding_function=embedding_fn)


def ingest_docs():
    print(f"Ingesting {len(DOCS)} documents...\n")

    for doc in DOCS:
        print(f"   Embedding: [{doc['id']}] {doc['title']}")
        text_to_embed = f"{doc['title']}\n\n{doc['content']}"

        collection.add(
            ids=[doc["id"]],
            documents=[text_to_embed],
            metadatas=[{"title": doc["title"], "id": doc["id"]}]
        )
    
    print(f"\n Done. {len(DOCS)} documents stored in ChromaDB")


if __name__ == "__main__":
    ingest_docs()