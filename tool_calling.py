from openai import OpenAI

client = OpenAI()


def multiply(a, b):
    return a * b


tools = [
    {
        "type": "function",
        "name": "multiply",
        "description": "Multiply two numbers together.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number"
                },
                "b": {
                    "type": "number"
                }
            },
            "required": ["a", "b"],
            "additionalProperties": False
        }
    }
]


response = client.responses.create(
    model="gpt-5.6-luna",
    input="What is 847 multiplied by 293?",
    tools=tools
)


for item in response.output:
    print(item)