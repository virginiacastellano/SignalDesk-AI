from celery import Celery

from app.core.config import settings

celery_app = Celery(
    "signaldesk",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.workers.tasks"],
)
celery_app.conf.update(task_routes={"app.workers.tasks.*": {"queue": "automation"}})
