from celery import Celery
from src.core import get_settings

celery = Celery(
    "tasks",
    broker=f"redis://{get_settings().REDIS_HOST}:{get_settings().REDIS_PORT}",
    include=["src.tasks.tasks"]
)

celery.conf.update(
    result_backend=f"redis://{get_settings().REDIS_HOST}:{get_settings().REDIS_PORT}/0",
    broker_connection_retry_on_startup=True,
)