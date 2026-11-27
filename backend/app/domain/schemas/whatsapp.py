from pydantic import BaseModel


class WhatsAppTextMessage(BaseModel):
    to: str
    body: str


class WhatsAppTemplateMessage(BaseModel):
    to: str
    template_name: str
    language_code: str = "es_AR"
    components: list[dict] = []


class WhatsAppSimulationRequest(BaseModel):
    phone: str
    message: str


class WhatsAppInteractiveReplyRequest(BaseModel):
    conversation_id: str
    option_id: str
    option_title: str
