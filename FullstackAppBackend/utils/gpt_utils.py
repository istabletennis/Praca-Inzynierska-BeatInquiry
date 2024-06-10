from openai import OpenAI
client = OpenAI(
    api_key="INSERT YOUR OWN KEY",
    organization='org-Obvh0GcONpcvGWp0XQ4NeLrO'
)


def send_prompt(prompt: str, model: str) -> str:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )
    response = chat_completion.choices[0].message.content
    return response
