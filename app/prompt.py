import ollama


def prompt(query):
    messages = []
    messages.append(
        {
            "role": "user",
            "content": f"Give me a recipe for {query} that includes the sections ingredients, instructions, and tips, in that order. Return the response in this format: title: <title>, contents: ingredients, instructions, tips. The title of the recipe must start with 'title:'. The section names must be in lowercase.",
        }
    )

    response = ollama.chat(
        model="llama3.2",
        messages=messages,
    )
    return response["message"]["content"]


if __name__ == "__main__":
    res = prompt("pizza")
    print(res)
