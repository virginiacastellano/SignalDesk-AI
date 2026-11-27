from pydantic import BaseModel


class WorkflowCreate(BaseModel):
    name: str
    trigger: str
    conditions: dict = {}
    actions: list[dict] = []
    is_active: bool = True


class WorkflowRead(WorkflowCreate):
    id: str

    model_config = {"from_attributes": True}
