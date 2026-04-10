import json
from openai import OpenAI

client = OpenAI()

def ask_llm(user_message, context):
    system_instructions = """
You are a dining assistant for Virginia Tech.

- The current time is provided in the context as `requested_time`.
- Use ONLY the hours and units provided in the context.
- Do NOT ask the user for the date or time.
- If `requested_time` is present, assume it is correct.
- If hours are provided, determine which locations are open at that time.
- Do NOT mention locations that are not included in the context.
"""

    messages = [
        {"role": "system", "content": system_instructions},
        {"role": "system", "content": f"CONTEXT:\n{json.dumps(context, indent=2)}"},
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    return response.choices[0].message.content
