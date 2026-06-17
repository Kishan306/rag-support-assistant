import anthropic
import logging
import time
from datetime import datetime, timezone, timedelta
import sys
from dotenv import load_dotenv
from query import retrieve

load_dotenv()
client = anthropic.Anthropic()


# logging setup
IST = timezone(timedelta(hours=5, minutes=30))
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("agent.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("agent")
logging.Formatter.converter = lambda *args: datetime.now(IST).timetuple()


# configuration
MAX_ITERATIONS = 5


# fake accounts database
FAKE_ACCOUNTS = {
    "alice@example.com": {"plan": "Pro", "status": "active", "projects": 7},
    "bob@example.com": {"plan": "Starter", "status": "active", "projects": 2},
    "charlie@example.com": {"plan": "Enterprise", "status": "suspended", "projects": 4}
}


# tool functions
def search_docs(query: str):
    chunks = retrieve(query, n_results=3)
    if not chunks:
        return "No relevant documentation found for this query."
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
        "divide": a / b if b !=0 else "Error: divide by zero"
    }
    return ops.get("operation", f"Error: unknown operation {operation}")

TOOL_FUNCTIONS = {
    "search_docs": search_docs,
    "lookup_account": lookup_account,
    "calculator": calculator
}


# tool definitions
tools = [
    {
        "name": "search_docs",
        "description": "Searches NovaSaaS product documentation for features, billing, refunds, account management, API access, integrations, and how-to guides. Use for general 'how do I' or 'what is' questions about the product.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "lookup_account",
        "description": "Looks up a specific user's account by email. Returns plan, status, and project count. Use only when a question is about a specific user's account identified by email.",
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
        "description": "Performs basic arithmetic on two numbers. Use for any math calculation.",
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
- For general product questions, use search_docs.
- For specific user account questions, use lookup_account.
- For math, use calculator.
- Answer general knowledge directly without tools.
Always base product answers on search_docs results. Never invent product details.
Be concise. Use plain text, no markdown."""


# tool execution with error handling
def execute_tool(name: str, tool_input: dict):
    """Run a tool function, catching any error so the loop never crashes."""
    func = TOOL_FUNCTIONS.get(name)
    if func is None:
        logger.error(f"Unknown tool requested: {name}")
        return f"Error: tool '{name}' does not exist"

    try:
        result = func(**tool_input)
        logger.info(f"Tool {name} succeeded")
        return result
    except Exception as e:
        logger.error(f"Tool {name} raised: {e}")
        return f"Error running {name}: {str(e)}"


# agentic loop
def run_agent(user_message: str):
    logger.info(f"New request: {user_message}")
    messages = [{"role": "user", "content": user_message}]

    for iteration in range(MAX_ITERATIONS):
        logger.info(f"Iteration {iteration + 1}/{MAX_ITERATIONS}")

        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=AGENT_SYSTEM,
                tools=tools,
                messages=messages
            )
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return f"Sorry, I hit an error contacting the model: {e}"

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            for block in response.content:
                if block.type == "text":
                    logger.info("Agent finished with final answer")
                    return block.text
            return "(no text response)"

        tool_results = []

        for block in response.content:
            if block.type == "tool_use":
                print(f"   {block.name}...", flush=True)
                logger.info(f"Executing {block.name} with {block.input}")

                result = execute_tool(block.name, block.input)

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result)
                })
        
        messages.append({"role": "user", "content": tool_results})

    logger.warning(f"Agent hit MAX_ITERATIONS ({MAX_ITERATIONS}) without finishing")
    return "I wasn't able to complete this request within the allowed steps. Please try rephrasing or contact support@novasaas.com."


if __name__ == "__main__":
    questions = [
        "How do I reset my password?",
        "Is charlie@example.com active, and how many projects times 5?",
        "What is the capital of France?"
    ]

    for q in questions:
        print("=" * 60)
        print(f"USER: {q}")
        print("AGENT:")
        answer = run_agent(q)
        print(f"AGENT: {answer}")
        print()
