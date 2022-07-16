from pydantic import BaseModel, HttpUrl


class FeedBase(BaseModel):
    title: str
    url: HttpUrl


class FeedCreate(FeedBase):
    pass


class Feed(FeedBase):
    id: int
    etag: str = ""
    last_modified: str = ""
    last_id: int = -1

    class Config:
        orm_mode = True


class ScraperBase(BaseModel):
    name: str
    regex: str


class ScraperCreate(ScraperBase):
    pass


class Scraper(ScraperBase):
    id: int
    feeds: list[Feed] = []

    class Config:
        orm_mode = True
