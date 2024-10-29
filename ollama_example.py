import ollama, time, sys

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": "Why is the sky blue?",
        },
    ],
)
# print(response["message"]["content"])
res = response["message"]["content"]

# typewriter print the response
for c in res:
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(0.01)
