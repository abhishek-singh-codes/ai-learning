from openai import OpenAI
import json

client = OpenAI()


# --------------------
# Actual Python tools
# --------------------

def multiply(a, b):
    return a * b


def add(a, b):
    return a + b


# --------------------
# Tell GPT about tools
# --------------------

tools = [
    {
        "type": "function",
        "name": "multiply",
        "description": "Multiply two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "add",
        "description": "Add two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["a", "b"],
            "additionalProperties": False
        }
    }
]


# --------------------
# User gives a goal
# --------------------

user_input = input("You: ")

response = client.responses.create(
    model="gpt-5.6-luna",
    input=user_input,
    tools=tools
)

print(response.output)


# --------------------
# Agent loop
# --------------------

while True:

    tool_calls = [
        item
        for item in response.output
        if item.type == "function_call"
    ]

    # No tool call means GPT is finished
    if not tool_calls:
        print("\nFinal answer:")
        print(response.output_text)
        break

    tool_outputs = []

    for tool_call in tool_calls:

        function_name = tool_call.name
        arguments = json.loads(tool_call.arguments)

        print("\nGPT selected:", function_name)
        print("Arguments:", arguments)

        # Execute the requested tool
        if function_name == "multiply":

            result = multiply(
                arguments["a"],
                arguments["b"]
            )

        elif function_name == "add":

            result = add(
                arguments["a"],
                arguments["b"]
            )

        else:
            result = "Unknown tool"

        print("Tool result:", result)

        # Prepare result for GPT
        tool_outputs.append({
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": str(result)
        })

    # Give tool results back to GPT
    response = client.responses.create(
        model="gpt-5.6-luna",
        previous_response_id=response.id,
        input=tool_outputs,
        tools=tools
    )