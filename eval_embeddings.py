import chromadb
from chromadb.utils import embedding_functions

chroma_client = chromadb.PersistentClient(path=".chromadb")
ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
collection = chroma_client.get_collection("novasaas_docs", embedding_function=ef)

GOLDEN_PAIRS = [
    {
        "question": "How do I reset my password?",
        "expected_chunk": "account-chunk-0",
        "expected_doc": "account"
    },
    {
        "question": "What is the refund policy?",
        "expected_chunk": "billing-chunk-3",
        "expected_doc": "billing"
    },
    {
        "question": "How much does the Pro plan cost?",
        "expected_chunk": "billing-chunk-0",
        "expected_doc": "billing"
    },
    {
        "question": "Can I use the API on a free plan?",
        "expected_chunk": "technical-chunk-0",
        "expected_doc": "technical"
    },
    {
        "question": "How do I add a team member?",
        "expected_chunk": "account-chunk-2",
        "expected_doc": "account"
    },
    {
        "question": "Does NovaSaaS support Slack?",
        "expected_chunk": "technical-chunk-2",
        "expected_doc": "technical"
    },
    {
        "question": "What payment methods are accepted?",
        "expected_chunk": "billing-chunk-4",
        "expected_doc": "billing"
    },
    {
        "question": "How do I enable two factor authentication?",
        "expected_chunk": "account-chunk-1",
        "expected_doc": "account"
    },
]

def evaluate():
    print(f"Running retrieval eval on {len(GOLDEN_PAIRS)} questions...\n")

    top1_correct = 0
    top3_correct = 0
    doc_correct = 0

    for pair in GOLDEN_PAIRS:
        results = collection.query(
            query_texts=[pair["question"]],
            n_results=3,
            include=["distances"]
        )

        retrieved_ids = results["ids"][0]
        distances = results["distances"][0]

        is_top1 = retrieved_ids[0] == pair["expected_chunk"]
        is_top3 = pair["expected_chunk"] in retrieved_ids
        is_doc_correct = any(
            pair["expected_doc"] in rid for rid in retrieved_ids
        )

        if is_top1: top1_correct += 1
        if is_top3: top3_correct += 1
        if is_doc_correct: doc_correct += 1

        status = "top1" if is_top1 else ("top3" if is_top3 else "nottop")
        print(f"{status} [{distances[0]:.3f}] {pair['question'][:50]}")
        if not is_top1:
            print(f"  Expected: {pair['expected_chunk']}")
            print(f"  Got:      {retrieved_ids[0]} (dist: {distances[0]:.3f})")

    total = len(GOLDEN_PAIRS)
    print(f"\n--- Results ---")
    print(f"Top-1 accuracy: {top1_correct}/{total} ({100*top1_correct//total}%)")
    print(f"Top-3 accuracy: {top3_correct}/{total} ({100*top3_correct//total}%)")
    print(f"Doc accuracy:   {doc_correct}/{total} ({100*doc_correct//total}%)")

    print(f"\n--- What this means ---")
    print(f"Top-1: exact right chunk was first result")
    print(f"Top-3: right chunk appeared somewhere in top 3")
    print(f"Doc:   at least one chunk from right document retrieved")

if __name__ == "__main__":
    evaluate()