from __future__ import absolute_import, unicode_literals
from celery import Celery
from datetime import timedelta
from logger import setup_logzero

logger = setup_logzero("./log.txt", "INFO")

app = Celery("app",
             broker="redis://localhost",
             backend="redis://localhost",
             )


class Config:
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'Asia/Tokyo'
    worker_max_tasks_per_child = 1,
    enable_utc = True,
    beat_schedule = {
            'run-every-3-minutes': {
                'task': 'tasks.scrapy_run_crawl',
                'schedule': timedelta(minutes=1),
                }
            }


app.config_from_object(Config)


if __name__ == "__main__":
    app.start()
