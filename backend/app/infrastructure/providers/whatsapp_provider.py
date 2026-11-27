import httpx

from app.core.config import settings
from app.core.logging import logger


class WhatsAppProvider:
    base_url = "https://graph.facebook.com/v20.0"

    async def send_text(self, *, to: str, body: str) -> dict:
        if not settings.whatsapp_access_token or not settings.whatsapp_phone_number_id:
            logger.warning("whatsapp.mocked_send", to=to)
            return {"id": "mock-message-id", "status": "mocked", "to": to, "body": body}

        url = f"{self.base_url}/{settings.whatsapp_phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"preview_url": False, "body": body},
        }
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                url,
                json=payload,
                headers={"Authorization": f"Bearer {settings.whatsapp_access_token}"},
            )
            response.raise_for_status()
            return response.json()

    async def send_template(self, *, to: str, template_name: str, language_code: str, components: list[dict]) -> dict:
        if not settings.whatsapp_access_token or not settings.whatsapp_phone_number_id:
            return {"id": "mock-template-id", "status": "mocked", "to": to, "template": template_name}

        url = f"{self.base_url}/{settings.whatsapp_phone_number_id}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code},
                "components": components,
            },
        }
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(url, json=payload, headers={"Authorization": f"Bearer {settings.whatsapp_access_token}"})
            response.raise_for_status()
            return response.json()
