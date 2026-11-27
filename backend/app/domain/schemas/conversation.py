from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    conversation_id: str
    content: str
    recipient_phone: str | None = None


class MessageRead(BaseModel):
    id: str
    direction: str
    sender_type: str
    content: str
    status: str
    meta: dict = {}
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationRead(BaseModel):
    id: str
    lead_id: str
    status: str
    bot_enabled: bool
    last_message_at: datetime | None
    messages: list[MessageRead] = []

    model_config = {"from_attributes": True}
