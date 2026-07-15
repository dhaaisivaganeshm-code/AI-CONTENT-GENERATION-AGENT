from fastapi import APIRouter, Depends

from app.dependencies import get_current_user

from app.schemas.chat import (
    CreateChatResponse,
    ChatSchema,
    SendMessageRequest,
    SendMessageResponse,
    RenameChatRequest,
    DeleteChatRequest,
    SuccessResponse
)

from app.services import chat_service


router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("/create", response_model=CreateChatResponse)
async def create_chat(
    user=Depends(get_current_user)
):
    return await chat_service.create_chat(user["_id"])


@router.get("/list", response_model=list[ChatSchema])
async def load_chats(
    user=Depends(get_current_user)
):
    return await chat_service.list_chats(user["_id"])


@router.post("/send", response_model=SendMessageResponse)
async def send_message(
    body: SendMessageRequest,
    user=Depends(get_current_user)
):
    reply = await chat_service.send_message(
        user["_id"],
        body.chatId,
        body.message
    )

    return SendMessageResponse(reply=reply)


@router.post("/rename", response_model=SuccessResponse)
async def rename_chat(
    body: RenameChatRequest,
    user=Depends(get_current_user)
):
    await chat_service.rename_chat(
        user["_id"],
        body.id,
        body.name
    )

    return SuccessResponse()


@router.post("/delete", response_model=SuccessResponse)
async def delete_chat(
    body: DeleteChatRequest,
    user=Depends(get_current_user)
):
    await chat_service.delete_chat(
        user["_id"],
        body.id
    )

    return SuccessResponse()