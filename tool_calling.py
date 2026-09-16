from openai import OpenAI
import json

client = OpenAI()


def multiply(a, b):
    return a * b


def add(a, b):
    return a + b


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

user_input = input("You: ")

response = client.responses.create(
    model="gpt-5.6-luna",
    input=user_input,
    tools=tools
)

print("\nFull GPT output:")
print(response.output)

for item in response.output:

    if item.type == "function_call":

        function_name = item.name
        arguments = json.loads(item.arguments)

        print("GPT selected tool:", function_name)
        print("Arguments:", arguments)

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

        print("Tool result:", result)