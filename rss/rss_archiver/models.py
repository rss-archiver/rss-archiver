from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    url = Column(String, unique=True, index=True)
    etag = Column(String, default="")
    last_modified = Column(String, default="")
    last_id = Column(Integer, default=-1)

    scrapers = relationship(
        "Scraper", secondary="feed_scraper_rel", back_populates="feeds"
    )


class Scraper(Base):
    __tablename__ = "scrapers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    regex = Column(String, index=True)

    feeds = relationship(
        "Feed", secondary="feed_scraper_rel", back_populates="scrapers"
    )


class FeedScraperRel(Base):
    __tablename__ = "feed_scraper_rel"

    feed_id = Column(Integer, ForeignKey("feeds.id"), primary_key=True)
    scraper_id = Column(Integer, ForeignKey("scrapers.id"), primary_key=True)
