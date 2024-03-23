from openai import OpenAI
from openai import OpenAI
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

def make_perplexity_call(language, phrase):

    question = "Please explain what the phrase " + phrase + " means. First give me a brief explanation, no more than a sentence. Then give a more elaborate description. Separate these two descriptions with the text 404_404. Ensure these descriptions are in " + language + "."
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
                question
            ),
        },
    ]

    client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

    # chat completion without streaming
    response = client.chat.completions.create(
        model="mistral-7b-instruct",
        messages=messages,
    )

    # print(response)
    answer = (response.choices[0].message.content)
    responses = answer.strip().split("404_404")
    # print(responses)
    
    return responses

