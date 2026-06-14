import anthropic
from dotenv import load_dotenv
from query import retrieve

load_dotenv()
client = anthropic.Anthropic()

FAKE_ACCOUNTS = {
    "alice@example.com": {"plan": "Pro", "status": "active", "projects": 7},
    "bob@example.com": {"plan": "Starter", "status": "active", "projects": 2},
    "charlie@example.com": {"plan": "Enterprise", "status": "suspended", "projects": 4},
}

def search_docs(query: str):
    """Search NovaSaaS documentation and return relevant chunks."""
    chunks = retrieve(query, n_results=3)
    if not chunks:
        return "No relevant documentation found for this query."
    # Return the text of retrieved chunks
    return "\n\n".join([f"[{c['title']}] {c['content']}" for c in chunks])

def lookup_account(email: str):
    account = FAKE_ACCOUNTS.get(email.lower())
    if account is None:
        return f"No account found for {email}"
    return account

def calculator(operation: str, a: float, b: float):
    ops = {
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "Error: divide by zero"
    }
    return ops.get(operation, f"Error: unknown operation {operation}")

TOOL_FUNCTIONS = {
    "search_docs": search_docs,
    "lookup_account": lookup_account,
    "calculator": calculator,
}

tools = [
    {
        "name": "search_docs",
        "description": "Searches the NovaSaaS product documentation for information about features, billing, refunds, account management, API access, integrations, and how-to guides. Use this for any general 'how do I' or 'what is' question about the product.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query describing what information to find"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "lookup_account",
        "description": "Looks up a specific user's account details by email address. Returns their plan, account status, and project count. Use this only when a question is about a specific user's account, identified by an email address.",
        "input_schema": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "The user's email address"}
            },
            "required": ["email"]
        }
    },
    {
        "name": "calculator",
        "description": "Performs basic arithmetic operations on two numbers. Use for any math calculation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The operation to perform"
                },
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["operation", "a", "b"]
        }
    }
]

AGENT_SYSTEM = """You are a NovaSaaS support agent with access to tools.

- For general product questions (how-to, features, billing policy), use search_docs.
- For questions about a specific user's account, use lookup_account.
- For math, use calculator.
- Answer general knowledge directly without tools.

Always base product answers on what search_docs returns. Never make up product details.
Be concise and helpful. Use plain text, no markdown."""


def run_agent(user_message: str):
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            system=AGENT_SYSTEM,
            tools=tools,
            messages = messages
        )

        print(f"\n[stop_reason: {response.stop_reason}]")
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            for block in response.content:
                if block.type == "text":
                    return block.text
            return "(no text response)"

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f" -> {block.name}({block.input})")
                func = TOOL_FUNCTIONS[block.name]
                result = func(**block.input)
                log_result = str(result)[:80] + "..." if len(str(result)) > 80 else str(result)
                print(f" <- {log_result}")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })

        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    questions = [
        "How do I reset my password?",
        "What plan is alice@example.com on ?",
        "What is the refund policy?",
        "Is charlie@example.com active, and how many projects do they have times 5?",
        "What is the capital of France?"
    ]

    for q in questions:
        print("=" * 60)
        print(f"USER: {q}")
        answer = run_agent(q)
        print(f"\nANSWER: {answer}")
        print()