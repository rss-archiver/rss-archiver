import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, HttpUrl


class Entry(BaseModel):
    id: str
    title: str
    author: str
    summary: str
    published: str
    link: HttpUrl


app = FastAPI(title="HTML-Archiver")


@app.post("/entry", response_class=HTMLResponse)
def add_entry(entry: Entry):
    response = httpx.get(entry.link)
    with open(f"[{entry.author}]{entry.title}.html", "w", encoding="utf8") as file:
        file.write(response.text)
    return response.text
