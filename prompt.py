import ollama


def prompt(query):
    messages = []
    messages.append(
        {
            "role": "user",
            "content": f"Give me a recipe for {query}",
        }
    )

    response = ollama.chat(
        model="llama3.2",
        messages=messages,
    )
    return response["message"]["content"]
