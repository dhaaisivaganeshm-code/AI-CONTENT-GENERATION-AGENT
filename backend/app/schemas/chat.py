from pydantic import BaseModel, ConfigDict, Field


class MessageSchema(BaseModel):
    id: str
    role: str
    content: str
    timestamp: str


class ChatSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    createdAt: str
    updatedAt: str
    pinned: bool = False
    favorited: bool = False
    messages: list[MessageSchema] = Field(default_factory=list)


class CreateChatResponse(BaseModel):
    id: str
    title: str
    createdAt: str


class SendMessageRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chatId: str
    message: str = Field(
        min_length=1,
        max_length=4000,
    )


class SendMessageResponse(BaseModel):
    reply: str


class RenameChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str = Field(
        min_length=1,
        max_length=60,
    )


class DeleteChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str


class SuccessResponse(BaseModel):
    success: bool = True