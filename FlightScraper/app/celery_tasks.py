from __future__ import absolute_import, unicode_literals
from celery import Celery
from datetime import timedelta
from logger import setup_logzero

logger = setup_logzero("./log.txt", "INFO")

app = Celery("celery",
             broker="redis://localhost",
             backend="redis://localhost",
             include="app.tasks")


class Config:
    task_serializer = 'json'
    result_serializer = 'json'
    accept_content = ['json']
    timezone = 'Asia/Tokyo'
    enable_utc = True,
    worker_max_tasks_per_child = 1,
    beat_schedule = {
            'run-every-3-minutes': {
                'task': 'tasks.scrapy_run_crawl',
                'schedule': timedelta(minutes=1),
                }
            }


app.config_from_object(Config)
app.autodiscover_tasks(['FlightScraper.tasks'], force=True)


if __name__ == "__main__":
    app.start()
