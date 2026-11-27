from app.core.logging import logger
from app.workers.celery_app import celery_app


@celery_app.task(name="app.workers.tasks.send_follow_up")
def send_follow_up(tenant_id: str, lead_id: str, template_name: str) -> dict:
    logger.info("workflow.follow_up.enqueued", tenant_id=tenant_id, lead_id=lead_id, template=template_name)
    return {"tenant_id": tenant_id, "lead_id": lead_id, "template": template_name, "status": "queued"}


@celery_app.task(name="app.workers.tasks.sync_google_sheets")
def sync_google_sheets(tenant_id: str) -> dict:
    logger.info("integration.google_sheets.mock_sync", tenant_id=tenant_id)
    return {"tenant_id": tenant_id, "rows_synced": 128, "status": "success"}
