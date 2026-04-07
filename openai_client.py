import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("PPLX_API_KEY"),
    base_url="https://api.perplexity.ai",
    )

def ask_openai(prompt: str) -> str:
    response = client.chat.completions.create(
        model="sonar",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content