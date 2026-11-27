from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    active_conversations: int
    total_leads: int
    conversion_rate: float
    ai_resolution_rate: float
    avg_response_seconds: int
    messages_today: int
    revenue_pipeline: int
    bot_health: str
