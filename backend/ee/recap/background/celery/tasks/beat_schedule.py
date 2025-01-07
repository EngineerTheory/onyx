from datetime import timedelta
from typing import Any

from recap.background.celery.tasks.beat_schedule import (
    tasks_to_schedule as base_tasks_to_schedule,
)
from recap.configs.constants import RecapCeleryTask

ee_tasks_to_schedule = [
    {
        "name": "autogenerate_usage_report",
        "task": RecapCeleryTask.AUTOGENERATE_USAGE_REPORT_TASK,
        "schedule": timedelta(days=30),  # TODO: change this to config flag
    },
    {
        "name": "check-ttl-management",
        "task": RecapCeleryTask.CHECK_TTL_MANAGEMENT_TASK,
        "schedule": timedelta(hours=1),
    },
]


def get_tasks_to_schedule() -> list[dict[str, Any]]:
    return ee_tasks_to_schedule + base_tasks_to_schedule
