import json
import anthropic
from dotenv import load_dotenv
from query import retrieve, generate

load_dotenv()
client = anthropic.Anthropic()

EVALUATOR_PROMPT = """You are evaluating a RAG support system's answer quality.

Given a question, the retrieved context, and the generated answer,
score the answer on three dimensions:

FAITHFULNESS (1-3):
1 = answer contains claims not supported by the context (hallucination)
2 = answer mostly grounded, minor unsupported claims
3 = answer fully grounded in the provided context

RELEVANCE (1-3):
1 = answer does not address the question asked
2 = answer partially addresses the question
3 = answer directly and completely addresses the question

CONCISENESS (1-3):
1 = answer is padded, repetitive, or unnecessarily long
2 = answer is acceptable length
3 = answer is appropriately concise

Reply with only valid JSON, no other text:
{"faithfulness": X, "relevance": X, "conciseness": X, "reasoning": "one sentence"}"""


TEST_CASES = [
    {
        "question": "How do I reset my password?",
        "must_contain": ["forgot password", "login"],
        "must_not_contain": [],
    },
    {
        "question": "What is the refund policy?",
        "must_contain": ["14", "refund"],
        "must_not_contain": [],
    },
    {
        "question": "How much does the Pro plan cost?",
        "must_contain": ["799", "pro"],
        "must_not_contain": [],
    },
    {
        "question": "Can I use the API on a free plan?",
        "must_contain": ["pro", "enterprise"],
        "must_not_contain": ["free", "starter"],
    },
    {
        "question": "How do I add a team member?",
        "must_contain": ["settings", "invite"],
        "must_not_contain": [],
    },
    {
        "question": "What is the weather in Mumbai?",
        "must_contain": ["don't have", "docs"],
        "must_not_contain": [],
    },
]


def evaluate_answer(question: str, context: str, answer: str) -> dict:
    """Ask Claude to score a RAG answer"""
    prompt = f"""Question: {question}

Retrieved context:
{context}

Generated answer:
{answer}"""

    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=200,
            temperature=0,
            system=EVALUATOR_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response.content[0].text.strip()
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"faithfulness": 0, "relevance": 0, "conciseness": 0, "reasoning": "parse error"}
    except Exception as e:
        return {"faithfulness": 0, "relevance": 0, "conciseness": 0, "reasoning": str(e)}


def check_assertions(answer: str, must_contain: list, must_not_contain: list) -> dict:
    """Check if answer contains required terms and avoids forbidden ones."""
    answer_lower = answer.lower()

    passed = []
    failed = []

    for term in must_contain:
        if term.lower() in answer_lower:
            passed.append(f"contains '{term}")
        else:
            failed.append(f"missing '{term}")

    for term in must_not_contain:
        if term.lower() in answer_lower:
            passed.append(f"should not contain '{term}")
        else:
            failed.append(f"avoids '{term}")

    return {
        "passed": passed,
        "failed": failed,
        "assertion_pass": len(failed) == 0
    }


def run_eval():
    print("=" * 60)
    print("RAG SYSTEM EVALUATION")
    print("=" * 60)

    total_faithfulness = 0
    total_relevance = 0
    total_conciseness = 0
    assertion_passes = 0

    for i, test in enumerate(TEST_CASES):
        question = test["question"]
        print(f"\n[{i+1}/{len(TEST_CASES)}] {question}")
        print("-" * 60)

        chunks = retrieve(question, n_results=3)

        if not chunks:
            answer = "I don't have that information in our docs"
            context = ""
        else:
            context = "\n\n".join([c["content"] for c in chunks])
            answer = generate(question, chunks)

        print(f"Answer: {answer[:120]}{'...'  if len(answer)>120 else ''}")

        scores = evaluate_answer(question, context, answer)
        total_faithfulness += scores.get("faithfulness", 0)
        total_relevance += scores.get("relevance", 0)
        total_conciseness += scores.get("conciseness", 0)

        print(f"Scores → faithfulness: {scores.get('faithfulness')}/3  "
              f"relevance: {scores.get('relevance')}/3  "
              f"conciseness: {scores.get('conciseness')}/3")
        print(f"Reasoning: {scores.get('reasoning', '')}")


        assertions = check_assertions(
            answer,
            test["must_contain"],
            test["must_not_contain"]
        )
        assertion_status = "PASS" if assertions["assertion_pass"] else "FAIL"
        print(f"Assertions: {assertion_status}")
        for item in assertions["failed"]:
            print(f"   {item}")

        if assertions["assertion_pass"]:
            assertion_passes += 1


    n = len(TEST_CASES)
    print("\n" + "=" * 65)
    print("SUMMARY")
    print("=" * 65)
    print(f"Faithfulness:  {total_faithfulness}/{n*3}  avg: {total_faithfulness/n:.1f}/3")
    print(f"Relevance:     {total_relevance}/{n*3}  avg: {total_relevance/n:.1f}/3")
    print(f"Conciseness:   {total_conciseness}/{n*3}  avg: {total_conciseness/n:.1f}/3")
    print(f"Assertions:    {assertion_passes}/{n} passed")
    overall = (total_faithfulness + total_relevance + total_conciseness) / (n * 9) * 100
    print(f"Overall score: {overall:.0f}%")

if __name__ == "__main__":
    run_eval()