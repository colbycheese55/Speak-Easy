from openai import OpenAI
from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

YOUR_API_KEY = os.environ.get("PERPLEX_API_KEY")

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
            "What does my boss mean when he says lets not move the goal posts?"
        ),
    },
]

client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

# chat completion without streaming
response = client.chat.completions.create(
    model="mistral-7b-instruct",
    messages=messages,
)
print(response)

