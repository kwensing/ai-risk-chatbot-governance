import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("PPLX_API_KEY"),
    base_url="https://api.perplexity.ai",
)

def get_response(user_input: str) -> str:
    """
    Call the LLM and return its text response.
    """
    ## return f"(Stub response, echoing your input) {user_input}"
    
    response = client.chat.completions.create(
        model="sonar",
        messages=[
            {"role": "system", "content": "You are a helpful AI Governance Associate."},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content