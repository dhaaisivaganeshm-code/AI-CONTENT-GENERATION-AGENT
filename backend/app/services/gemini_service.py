import google.generativeai as genai

from app.config import settings


genai.configure(api_key=settings.gemini_api_key)

model = genai.GenerativeModel(
    model_name=settings.gemini_model
)


SYSTEM_PROMPT = """
You are an AI Content Assistant.

You help users:
- Write blogs
- Rewrite text
- Generate emails
- Summarize content
- Brainstorm ideas
- Improve grammar

Always provide clear, concise, professional responses.
"""


async def generate_reply(
    history: list[dict],
    user_message: str,
) -> str:

    try:
        chat = model.start_chat(history=[])

        for message in history:
            chat.send_message(
                message["content"]
            )

        response = chat.send_message(
            f"{SYSTEM_PROMPT}\n\n{user_message}",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.9,
                "max_output_tokens": 1024,
            },
        )

        return response.text.strip()

    except Exception as e:
        print(f"Gemini Error: {e}")
        return (
            "Sorry, I couldn't generate a response "
            "at the moment. Please try again."
        )