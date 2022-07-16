import logging

import celery
import feedparser
import httpx
from celery import Celery
from celery.schedules import crontab
from celery.utils.log import get_task_logger

from . import crud
from .database import SessionLocal

logger = get_task_logger(__name__)
logger.propagate = True
db = SessionLocal()
app = Celery(
    "worker",
    backend="redis://:password123@redis:6379/0",
    broker="amqp://user:bitnami@rabbitmq:5672//",
)
app.conf.update(task_track_started=True)


@celery.signals.after_setup_logger.connect
def on_after_setup_logger(**kwargs):
    logger = logging.getLogger("celery")
    logger.propagate = True
    logger = logging.getLogger("celery.app.trace")
    logger.propagate = True


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(minute="*/5"),
        update_feeds.s(),
    )


@app.task
def update_feeds():
    feeds = crud.get_feeds(db)
    for feed in feeds:
        logger.info(f"Updating {feed.title}")
        parsed_feed = feedparser.parse(
            feed.url, modified=feed.last_modified, etag=feed.etag
        )
        if parsed_feed.entries:
            feed.etag = getattr(feed, "etag", feed.etag)
            feed.last_modified = getattr(feed, "modified", feed.last_modified)
            for scraper in feed.scrapers:
                for entry in parsed_feed.entries:
                    if entry.id == feed.last_id:
                        break
                    httpx.post(f"http://{scraper.name}:8000/entry", json=entry)
            feed.last_id = parsed_feed.entries[0].id
    return "Success"
