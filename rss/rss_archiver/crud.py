from sqlalchemy.orm import Session

from . import models, schemas


def get_feed(db: Session, feed_id: int) -> models.Feed:
    return db.query(models.Feed).filter(models.Feed.id == feed_id).first()


def get_feeds(db: Session, skip: int = 0, limit: int = 100) -> list[models.Feed]:
    return db.query(models.Feed).offset(skip).limit(limit).all()


def create_feed(db: Session, feed: schemas.FeedCreate) -> models.Feed:
    db_item = models.Feed(**feed.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_feed(db: Session, feed_id: int) -> models.Feed:
    db_feed = db.query(models.Feed).filter(models.Feed.id == feed_id)
    db_feed.delete()
    db.commit()
    return db_feed


def get_scraper(db: Session, scraper_id: int) -> models.Scraper:
    return db.query(models.Scraper).filter(models.Scraper.id == scraper_id).first()


def get_scrapers(db: Session, skip: int = 0, limit: int = 100) -> list[models.Scraper]:
    return db.query(models.Scraper).offset(skip).limit(limit).all()


def create_scraper(db: Session, scraper: schemas.ScraperCreate) -> models.Scraper:
    db_scraper = models.Scraper(name=scraper.name, regex=scraper.regex)
    db.add(db_scraper)
    db.commit()
    db.refresh(db_scraper)
    return db_scraper


def delete_scraper(db: Session, scraper_id: int) -> models.Scraper:
    db_scraper = db.query(models.Scraper).filter(models.Scraper.id == scraper_id)
    db_scraper.delete()
    db.commit()
    return db_scraper
