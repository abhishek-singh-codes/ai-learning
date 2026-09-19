import json
import os


MEMORY_FILE = "./memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("memory.json empty or invalid hai. Fresh memory start kar rahe hain.")
        return []


def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=2)


memory = load_memory()

print("Current memory:")
print(memory)

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    if user_input.lower().startswith("remember "):
        fact = user_input[9:]

        memory.append(fact)
        save_memory(memory)

        print("AI: I will remember that.")
        continue

    if user_input.lower() == "show memory":
        print("AI:", memory)
        continue

    print("AI: I only know how to save and show memories.")