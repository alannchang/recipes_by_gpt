import ollama

messages = []

while True:
    full_response = ''
    prompt = input("How can I help you today? ")
    messages.append(
        {
            "role": "user",
            "content" : prompt,
        }
    )
    response = ollama.chat(
        model="llama3.2",
        messages=messages,
        stream=True,
    )

    for chunk in response:
        full_response += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)

    messages.append(
        {
            "role": "assistant",
            "content": full_response,
        }
    )

    print('\n')

