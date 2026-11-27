from openai import AsyncOpenAI

from app.core.config import settings
from app.core.logging import logger


class AIProvider:
    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    async def generate_reply(self, *, business_prompt: str, conversation: list[dict], user_message: str) -> dict:
        if not self.client:
            lower_message = user_message.lower()
            handoff_required = any(
                phrase in lower_message
                for phrase in ["humano", "asesor", "persona", "reclamo", "urgente", "hablar con alguien"]
            )
            wants_menu = any(
                phrase in lower_message
                for phrase in ["hola", "menu", "menú", "opciones", "ayuda", "no entiendo", "h"]
            )
            logger.warning("ai.mocked_response")
            if handoff_required:
                return {
                    "reply": "Entiendo. Te derivo con una persona del equipo para que pueda ayudarte con mas detalle.",
                    "handoff_required": True,
                    "intent": "human_handoff",
                    "interactive": None,
                }
            if wants_menu:
                return {
                    "reply": "Hola. Soy SignalDesk AI. Te puedo ayudar con estas opciones:",
                    "handoff_required": False,
                    "intent": "main_menu",
                    "interactive": {
                        "type": "list",
                        "title": "Menu Principal",
                        "button": "Ver opciones",
                        "sections": [
                            {
                                "title": "Atencion comercial",
                                "rows": [
                                    {"id": "pricing", "title": "Planes y precios", "description": "Comparar planes y solicitar una demo"},
                                    {"id": "demo", "title": "Agendar demo", "description": "Coordinar una llamada con ventas"},
                                    {"id": "human", "title": "Hablar con asesor", "description": "Derivar a una persona del equipo"},
                                ],
                            },
                            {
                                "title": "Soporte",
                                "rows": [
                                    {"id": "integrations", "title": "Integraciones", "description": "WhatsApp, CRM, Gmail y Sheets"},
                                    {"id": "faq", "title": "Preguntas frecuentes", "description": "Resolver dudas comunes"},
                                ],
                            },
                        ],
                    },
                }
            return {
                "reply": "Gracias por escribirnos. Ya tengo tu consulta y puedo ayudarte con precios, disponibilidad o coordinar una demo.",
                "handoff_required": False,
                "intent": "pricing_or_demo",
                "interactive": {
                    "type": "buttons",
                    "buttons": [
                        {"id": "pricing", "title": "Ver planes"},
                        {"id": "demo", "title": "Agendar demo"},
                        {"id": "human", "title": "Asesor"},
                    ],
                },
            }

        response = await self.client.responses.create(
            model=settings.openai_model,
            instructions=business_prompt,
            input=[
                *conversation[-12:],
                {"role": "user", "content": user_message},
            ],
        )
        text = response.output_text
        lower = text.lower()
        return {
            "reply": text,
            "handoff_required": any(word in lower for word in ["humano", "asesor", "reclamo", "urgente"]),
            "intent": "support",
            "interactive": None,
        }
