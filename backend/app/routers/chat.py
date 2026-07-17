from fastapi import APIRouter, Depends, status

from app.dependencies import get_current_user
from app.schemas.chat import (
    ChatSchema,
    CreateChatResponse,
    DeleteChatRequest,
    RenameChatRequest,
    SendMessageRequest,
    SendMessageResponse,
    SuccessResponse,
)
from app.services import chat_service

router = APIRouter(
    tags=["Chat"],
)


@router.post(
    "/create",
    response_model=CreateChatResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_chat(
    current_user: dict = Depends(get_current_user),
) -> CreateChatResponse:
    """Create a new chat for the authenticated user."""
    return await chat_service.create_chat(current_user["_id"])


@router.get(
    "/list",
    response_model=list[ChatSchema],
)
async def list_chats(
    current_user: dict = Depends(get_current_user),
) -> list[ChatSchema]:
    """Return all chats belonging to the authenticated user."""
    return await chat_service.list_chats(current_user["_id"])


@router.post(
    "/send",
    response_model=SendMessageResponse,
)
async def send_message(
    request: SendMessageRequest,
    current_user: dict = Depends(get_current_user),
) -> SendMessageResponse:
    """Send a message to a chat and receive an AI response."""

    reply = await chat_service.send_message(
        user_id=current_user["_id"],
        chat_id=request.chatId,
        message=request.message,
    )

    return SendMessageResponse(reply=reply)


@router.post(
    "/rename",
    response_model=SuccessResponse,
)
async def rename_chat(
    request: RenameChatRequest,
    current_user: dict = Depends(get_current_user),
) -> SuccessResponse:
    """Rename an existing chat."""

    await chat_service.rename_chat(
        user_id=current_user["_id"],
        chat_id=request.id,
        name=request.name,
    )

    return SuccessResponse()


@router.post(
    "/delete",
    response_model=SuccessResponse,
)
async def delete_chat(
    request: DeleteChatRequest,
    current_user: dict = Depends(get_current_user),
) -> SuccessResponse:
    """Delete a chat."""

    await chat_service.delete_chat(
        user_id=current_user["_id"],
        chat_id=request.id,
    )

    return SuccessResponse()