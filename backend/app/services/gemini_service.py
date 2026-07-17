import logging

from groq import Groq

from app.config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
You are AI Content Assistant.

Your responsibilities include:
- Writing blogs
- Writing articles
- Rewriting text
- Summarizing
- Drafting emails
- Brainstorming
- Grammar correction
- Professional writing

Always provide detailed and accurate responses.
"""

client = Groq(api_key=settings.ai_api_key)


async def generate_reply(
    history: list[dict],
    user_message: str,
) -> str:
    """
    Generate AI response using Groq.
    """

    try:
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            }
        ]

        # Add previous conversation
        for chat in history:
            if "role" in chat and "content" in chat:
                messages.append(
                    {
                        "role": chat["role"],
                        "content": chat["content"],
                    }
                )

        # Current user message
        messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        response = client.chat.completions.create(
            model=settings.ai_model,
            messages=messages,
            temperature=0.7,
            max_completion_tokens=1024,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.exception(e)
        return f"Groq Error: {str(e)}"