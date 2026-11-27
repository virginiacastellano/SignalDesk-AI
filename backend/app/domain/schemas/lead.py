from datetime import datetime

from pydantic import BaseModel


class LeadCreate(BaseModel):
    name: str
    phone: str
    email: str | None = None
    tags: list[str] = []


class LeadRead(LeadCreate):
    id: str
    lifecycle_stage: str
    source: str
    score: int
    created_at: datetime

    model_config = {"from_attributes": True}
