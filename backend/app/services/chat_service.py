from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException, status

from app import database
from app.services.gemini_service import generate_reply


def _now_iso() -> str:
    """Return the current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str = "id") -> str:
    """Generate a short unique ID."""
    return f"{prefix}_{uuid4().hex[:12]}"


def _serialize_chat(doc: dict) -> dict:
    """Convert a MongoDB document into the frontend response format."""
    return {
        "id": doc["_id"],
        "title": doc.get("title", "New chat"),
        "createdAt": doc.get("created_at"),
        "updatedAt": doc.get("updated_at"),
        "pinned": doc.get("pinned", False),
        "favorited": doc.get("favorited", False),
        "messages": doc.get("messages", []),
    }


def _check_database():
    """Ensure the database connection is available."""
    if database.db is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection is unavailable.",
        )


async def create_chat(user_id: str) -> dict:
    """Create a new chat."""
    _check_database()

    chat_id = _new_id()
    now = _now_iso()

    doc = {
        "_id": chat_id,
        "user_id": user_id,
        "title": "New chat",
        "created_at": now,
        "updated_at": now,
        "pinned": False,
        "favorited": False,
        "messages": [],
    }

    await database.db.chats.insert_one(doc)

    return {
        "id": chat_id,
        "title": "New chat",
        "createdAt": now,
    }


async def list_chats(user_id: str) -> list[dict]:
    """Return all chats for a user."""
    _check_database()

    cursor = database.db.chats.find(
        {"user_id": user_id}
    ).sort("updated_at", -1)

    return [_serialize_chat(doc) async for doc in cursor]


async def rename_chat(
    user_id: str,
    chat_id: str,
    name: str,
) -> None:
    """Rename a chat."""
    _check_database()

    result = await database.db.chats.update_one(
        {
            "_id": chat_id,
            "user_id": user_id,
        },
        {
            "$set": {
                "title": name.strip(),
                "updated_at": _now_iso(),
            }
        },
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )


async def delete_chat(
    user_id: str,
    chat_id: str,
) -> None:
    """Delete a chat."""
    _check_database()

    result = await database.db.chats.delete_one(
        {
            "_id": chat_id,
            "user_id": user_id,
        }
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )


async def send_message(
    user_id: str,
    chat_id: str,
    message: str,
) -> str:
    """Send a message and receive an AI-generated reply."""
    _check_database()

    chat = await database.db.chats.find_one(
        {
            "_id": chat_id,
            "user_id": user_id,
        }
    )

    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found.",
        )

    now = _now_iso()

    user_message = {
        "id": _new_id("msg"),
        "role": "user",
        "content": message,
        "timestamp": now,
    }

    history = chat.get("messages", [])

    try:
        reply_text = await generate_reply(
            history,
            message,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate AI response: {str(exc)}",
        )

    assistant_message = {
        "id": _new_id("msg"),
        "role": "assistant",
        "content": reply_text,
        "timestamp": _now_iso(),
    }

    update = {
        "$push": {
            "messages": {
                "$each": [
                    user_message,
                    assistant_message,
                ]
            }
        },
        "$set": {
            "updated_at": assistant_message["timestamp"],
        },
    }

    # Automatically set the chat title from the first message
    if not history:
        title = " ".join(message.split())

        if len(title) > 42:
            title = title[:42].rstrip() + "..."

        update["$set"]["title"] = title

    await database.db.chats.update_one(
        {
            "_id": chat_id,
            "user_id": user_id,
        },
        update,
    )

    return reply_text