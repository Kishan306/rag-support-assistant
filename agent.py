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


TOOL_FUNCTIONS = {
    "calculator": calculator
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
        "What is 23 multiplied by 47?",
        "What is 100 divided by 7?",
        "What is the capital of France?"
    ]

    for q in questions:
        print("="*55)
        print(f"USER: {q}")
        answer = run_agent(q)
        print(f"\nFinal Answer: {answer}")
        print()
