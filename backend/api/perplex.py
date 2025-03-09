from openai import OpenAI

#Not putting API key in a public repo
API_KEY = ""

def get_ai_response(prompt):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {
            "role": "user",
            "content": (
                prompt
            ),
        },
    ]

# Here you would typically call the AI model with the messages
# response = call_ai_model(messages)
# return response

    client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    return response

    """
    # chat completion with streaming
    response_stream = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
        stream=True,
    )
    for response in response_stream:
        print(response)"
    """