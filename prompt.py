import ollama


def prompt(query):
    messages = []
    messages.append(
        {
            "role": "user",
            "content": f"Give me a recipe for {query} that includes the sections ingredients, instructions, and tips, in that order",
        }
    )

    response = ollama.chat(
        model="llama3.2",
        messages=messages,
    )
    return response["message"]["content"]
