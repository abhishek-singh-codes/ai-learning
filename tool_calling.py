from openai import OpenAI
import json

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

#(arguments='{"a":847,"b":293}', call_id='call_hV8V2kI1JUoDJh4jK8oyVY6p', name='multiply', type='function_call', id='fc_06051fb4c16e6342006aaac3457e5487d1ab75c4c6c08e1a98', caller=None, namespace=None, status='completed')


for item in response.output:

    if item.type == "function_call":

        function_name = item.name
        arguments = json.loads(item.arguments)

        print("GPT wants to call:", function_name)
        print("Arguments:", arguments)

        if function_name == "multiply":
            result = multiply(
                arguments["a"],
                arguments["b"]
            )

            print("Tool result:", result)

            tool_result = {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": str(result)
            }

            final_response = client.responses.create(
                model="gpt-5.6-luna",
                previous_response_id=response.id,
                input=[tool_result],
                tools=tools
            )

            print("\nFinal answer:")
            print(final_response.output_text)