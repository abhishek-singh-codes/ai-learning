from openai import OpenAI
import json
import os
import numpy as np

client = OpenAI()

MEMORY_FILE = "memory.json"


# --------------------
# Load memories
# --------------------

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


# --------------------
# Convert text into embedding
# --------------------

def create_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding


# --------------------
# Calculate similarity
# --------------------

def cosine_similarity(vector_a, vector_b):
    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    return np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    )


# --------------------
# Find relevant memories
# --------------------

def find_relevant_memories(question, memories, top_k=2):
    question_embedding = create_embedding(question)

    scored_memories = []

    for memory in memories:
        memory_embedding = create_embedding(memory)

        score = cosine_similarity(
            question_embedding,
            memory_embedding
        )

        scored_memories.append((memory, score))

    scored_memories.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return scored_memories[:top_k]


# --------------------
# Main program
# --------------------

memories = load_memory()

print("Loaded memories:")
for memory in memories:
    print("-", memory)

question = input("\nAsk a question: ")

relevant_memories = find_relevant_memories(
    question,
    memories
)

print("\nRelevant memories:")

for memory, score in relevant_memories:
    print(f"{score:.4f} → {memory}")