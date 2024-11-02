import ollama


def prompt(query):
    messages = []
    messages.append(
        {
            "role": "user",
            "content": f"Give me a recipe for {query} that includes the sections ingredients, instructions, and tips, in that order. Return the response as a dictionary with keys 'Title', 'Ingredients', 'Instructions', and 'Tips'. Keep the values for each key section as a string.",
        }
    )

    response = ollama.chat(
        model="llama3.2",
        messages=messages,
    )
    return response["message"]["content"]


if __name__ == "__main__":
    print(prompt("pizza"))
