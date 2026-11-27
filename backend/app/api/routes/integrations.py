from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_current_identity
from app.workers.tasks import sync_google_sheets

router = APIRouter()


@router.get("")
async def list_integrations(_: Annotated[dict, Depends(get_current_identity)]):
    return [
        {"provider": "google_sheets", "status": "connected", "last_sync": "mock"},
        {"provider": "gmail", "status": "ready", "last_sync": "mock"},
        {"provider": "crm_webhook", "status": "connected", "last_sync": "mock"},
    ]


@router.post("/google-sheets/sync")
async def sync_sheets(identity: Annotated[dict, Depends(get_current_identity)]):
    task = sync_google_sheets.delay(identity["tenant_id"])
    return {"task_id": task.id, "status": "queued"}
