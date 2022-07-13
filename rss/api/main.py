"""Main module for rss-archiver"""
__version__ = 1
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/feeds/{feed_id}", response_model=schemas.Feed)
def read_feed(feed_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_feed(db, feed_id=feed_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/feeds/", response_model=schemas.Feed)
def create_feed(feed: schemas.FeedCreate, db: Session = Depends(get_db)):
    return crud.create_feed(db=db, feed=feed)


@app.get("/feeds/", response_model=list[schemas.Feed])
def read_feeds(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_feeds(db, skip=skip, limit=limit)
    return items
