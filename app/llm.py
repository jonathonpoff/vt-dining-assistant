import json
from openai import OpenAI

client = OpenAI()

def ask_llm(user_message, context):
    messages = [
        {"role": "system", "content": "You are a dining assistant for Virginia Tech."},
        {"role": "system", "content": f"CONTEXT:\n{json.dumps(context, indent=2)}"},
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content