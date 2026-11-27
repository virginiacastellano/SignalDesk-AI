from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.session import Base


def default_menu_sections() -> list[dict]:
    return [
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
    ]


def default_option_replies() -> dict:
    return {
        "pricing": {
            "content": "Tenemos tres planes: Starter para equipos chicos, Growth para automatizacion comercial y Scale para operaciones multiagente. Para recomendarte uno, contame cuantos mensajes reciben por dia.",
            "intent": "pricing_selected",
            "handoff_required": False,
        },
        "demo": {
            "content": "Perfecto. Te puedo agendar una demo de 20 minutos. Que horario te queda mejor: manana, tarde o noche?",
            "intent": "demo_selected",
            "handoff_required": False,
        },
        "human": {
            "content": "Listo, te derivo con una persona del equipo para continuar la conversacion.",
            "intent": "human_handoff",
            "handoff_required": True,
        },
        "integrations": {
            "content": "Podemos integrar WhatsApp con CRM, Google Sheets, Gmail y webhooks. Tambien se puede enviar cada lead calificado automaticamente al pipeline comercial.",
            "intent": "integrations_selected",
            "handoff_required": False,
        },
        "faq": {
            "content": "Preguntas frecuentes: tiempos de implementacion, templates aprobados, handoff humano, integraciones y metricas. Elegi una categoria o escribime tu duda.",
            "intent": "faq_selected",
            "handoff_required": False,
        },
    }


class BotConfig(Base):
    __tablename__ = "bot_configs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    tenant_id: Mapped[str] = mapped_column(ForeignKey("tenants.id"), unique=True, index=True)
    welcome_message: Mapped[str] = mapped_column(String(500), default="Hola. Soy SignalDesk AI. Te puedo ayudar con estas opciones:")
    fallback_message: Mapped[str] = mapped_column(String(500), default="Gracias por escribirnos. Ya tengo tu consulta y puedo ayudarte con precios, disponibilidad o coordinar una demo.")
    menu_title: Mapped[str] = mapped_column(String(120), default="Menu Principal")
    menu_button_label: Mapped[str] = mapped_column(String(40), default="Ver opciones")
    handoff_keywords: Mapped[list[str]] = mapped_column(JSON, default=lambda: ["humano", "asesor", "persona", "reclamo", "urgente", "hablar con alguien"])
    menu_keywords: Mapped[list[str]] = mapped_column(JSON, default=lambda: ["hola", "menu", "menú", "opciones", "ayuda", "no entiendo", "h"])
    menu_sections: Mapped[list[dict]] = mapped_column(JSON, default=default_menu_sections)
    option_replies: Mapped[dict] = mapped_column(JSON, default=default_option_replies)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
