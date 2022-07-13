from sqlalchemy.orm import Session

from . import models, schemas


def get_feed(db: Session, feed_id: int):
    return db.query(models.Feed).filter(models.Feed.id == feed_id).first()


def get_feed_by_url(db: Session, url: str):
    return db.query(models.Feed).filter(models.Feed.url == url).first()


def get_feeds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Feed).offset(skip).limit(limit).all()


def create_feed(db: Session, feed: schemas.FeedCreate):
    db_item = models.Feed(**feed.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
