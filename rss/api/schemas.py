from pydantic import BaseModel, HttpUrl


class FeedBase(BaseModel):
    title: str
    description: str | None = None
    url: HttpUrl


class FeedCreate(FeedBase):
    pass


class Feed(FeedBase):
    id: int

    class Config:
        orm_mode = True
