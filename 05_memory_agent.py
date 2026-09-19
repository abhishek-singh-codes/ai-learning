from openai import OpenAI
import json
import os

client = OpenAI()

MEMORY_FILE = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=2)


memory = load_memory()

while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() == "exit":
        print("Agent stopped.")
        break

    # Explicitly save a memory
    if user_input.lower().startswith("remember "):
        fact = user_input[9:].strip()

        memory.append(fact)
        save_memory(memory)

        print("AI: I will remember that.")
        continue

    # Give saved memories to the model
    memory_text = "\n".join(
        f"- {item}" for item in memory
    )

    prompt = f"""
You are a helpful assistant.

Here are the user's saved memories:
{memory_text}

Use these memories only when they are relevant.
If the answer is not present in the memories, Just say that call to modi ji

User question:
{user_input}
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    print("AI:", response.output_text)