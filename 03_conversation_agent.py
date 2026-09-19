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
# Tool descriptions for GPT
# --------------------

tools = [
    {
        "type": "function",
        "name": "multiply",
        "description": "Multiply two numbers.",
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
        "description": "Add two numbers.",
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
# Tool execution
# --------------------

def execute_tool(function_name, arguments):
    arguments = json.loads(arguments)

    if function_name == "multiply":
        return multiply(arguments["a"], arguments["b"])

    if function_name == "add":
        return add(arguments["a"], arguments["b"])

    return "Unknown tool"


# --------------------
# Conversation state
# --------------------

previous_response_id = None


# --------------------
# Outer loop: conversation loop
# --------------------

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        print("Agent stopped.")
        break

    # First request or continuation request
    if previous_response_id is None:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=user_input,
            tools=tools
        )
    else:
        response = client.responses.create(
            model="gpt-5.6-luna",
            previous_response_id=previous_response_id,
            input=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            tools=tools
        )

    # Inner loop: tool-calling loop
    while True:
        function_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # No tool call means final answer is ready
        if not function_calls:
            print("AI:", response.output_text)
            break

        # Execute every requested tool
        tool_outputs = []

        for function_call in function_calls:
            result = execute_tool(
                function_call.name,
                function_call.arguments
            )

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": function_call.call_id,
                    "output": str(result)
                }
            )

        # Send tool result back to GPT
        response = client.responses.create(
            model="gpt-5.6-luna",
            previous_response_id=response.id,
            input=tool_outputs,
            tools=tools
        )

    # Save latest response as conversation state
    previous_response_id = response.id