"""Main module for rss-archiver"""
__version__ = 1
import re

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
tags_metadata = [
    {
        "name": "Feeds",
        "description": "Operations with feeds.",
    },
    {
        "name": "Scrapers",
        "description": "Manage Scrapers.",
    },
]
app = FastAPI(title="RSS-Archiver", openapi_tags=tags_metadata)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/feeds/", response_model=schemas.Feed, tags=["Feeds"])
def create_feed(feed: schemas.FeedCreate, db: Session = Depends(get_db)):
    try:
        db_feed = crud.create_feed(db=db, feed=feed)
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Integrity Error")
    for scraper in crud.get_scrapers(db):
        if re.match(scraper.regex, feed.url):
            db_feed.scrapers.append(scraper)
    if not db_feed.scrapers:
        raise HTTPException(
            status_code=422,
            detail="The URL of the feed doesn't match any of the scraper regex's",
        )
    db.commit()
    return db_feed


@app.get("/feeds/", response_model=list[schemas.Feed], tags=["Feeds"])
def read_feeds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    feeds = crud.get_feeds(db, skip=skip, limit=limit)
    return feeds


@app.get("/feeds/{feed_id}", response_model=schemas.Feed, tags=["Feeds"])
def read_feed(feed_id: int, db: Session = Depends(get_db)):
    db_feed = crud.get_feed(db, feed_id=feed_id)
    if db_feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")
    return db_feed


@app.delete("/feeds/{feed_id}", response_model=schemas.Feed, tags=["Feeds"])
def delete_feed(feed_id: int, db: Session = Depends(get_db)):
    db_feed = crud.delete_feed(db, feed_id=feed_id)
    if db_feed is None:
        raise HTTPException(status_code=404, detail="Feed not found")
    return db_feed


@app.post("/scrapers/", response_model=schemas.Scraper, tags=["Scrapers"])
def create_scraper(scraper: schemas.ScraperCreate, db: Session = Depends(get_db)):
    return crud.create_scraper(db=db, scraper=scraper)


@app.get("/scrapers/", response_model=list[schemas.Scraper], tags=["Scrapers"])
def read_scrapers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_scrapers(db, skip=skip, limit=limit)


@app.get("/scrapers/{scraper_id}", response_model=schemas.Scraper, tags=["Scrapers"])
def read_scraper(scraper_id: int, db: Session = Depends(get_db)):
    db_scraper = crud.get_scraper(db, scraper_id=scraper_id)
    if db_scraper is None:
        raise HTTPException(status_code=404, detail="Scraper not found")
    return db_scraper


@app.delete("/scrapers/{scraper_id}", response_model=schemas.Scraper, tags=["Scrapers"])
def delete_scraper(scraper_id: int, db: Session = Depends(get_db)):
    db_scraper = crud.delete_scraper(db, scraper_id=scraper_id)
    if db_scraper is None:
        raise HTTPException(status_code=404, detail="Scraper not found")
    return db_scraper
