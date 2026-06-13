import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

def calculator(operation: str, a: float, b: float):
    if operation == "add":
        return a + b
    elif operation == "subtract": 
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            return "Error: cannot divide by zero"
        return a / b
    else:
        return f"Error: unknown operation {operation}"

def lookup_account(email: str):
    account = FAKE_ACCOUNTS.get(email.lower())
    if account is None:
        return f"No account found for {email}"
    return account

TOOL_FUNCTIONS = {
    "calculator": calculator,
    "lookup_account": lookup_account
}

FAKE_ACCOUNTS = {
    "alice@example.com": {"plan": "Pro", "status": "active", "projects": 7},
    "bob@example.com": {"plan": "Starter", "status": "active", "projects": 2},
    "charlie@example.com": {"plan": "Enterprise", "status": "suspended", "projects": 4}
}

tools = [
    {
        "name": "calculator",
        "description": "Performs basic arithmetic operations. Use this for any math calculation involving two numbers.",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The arithmetic operation to perform"
                },
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            "required": ["operation", "a", "b"]
        }
    },
    {
        "name": "lookup_account",
        "description": "Looks up a NovaSaaS user's account details by their email address. Returns their plan, account status, and number of projects. Use this whenever a question is about a specific user's account.",
        "input_schema": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The user's email address"
                }
            },
            "required": ["email"]
        }
    }
]


def run_agent(user_message: str):
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            tools=tools,
            messages=messages
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
                tool_name = block.name
                tool_input = block.input
                tool_id = block.id

                print(f" -> Model wants: {tool_name}({tool_input})")

                func = TOOL_FUNCTIONS[tool_name]
                result = func(**tool_input)

                print(f" <- Tool returned: {result}")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": str(result)
                })

        messages.append({"role": "user", "content": tool_results})


if __name__ == "__main__":
    questions = [
        "What is 88 times 12?",
        "What plan is kishan@example.com on?",
        "Is bob@example.com's account active?",
        "What is the capital of France?",
        "How many projects does alice@example.com have, and what is that number times 10?",
    ]

    for q in questions:
        print("="*55)
        print(f"USER: {q}")
        answer = run_agent(q)
        print(f"\nFinal Answer: {answer}")
        print()
