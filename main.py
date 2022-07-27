import json

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


class OutputPost(BaseModel):
    date: str
    title: str
    description: str
    url: str


class Posts(BaseModel):
    posts: list[OutputPost]


app = FastAPI(docs_url=None, redoc_url=None)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse, response_model=Posts)
async def index(request: Request):
    with open('settings.txt', encoding='utf8') as config:
        data = config.read()
        settings = json.loads(data)
    with open('projects.json', encoding='utf8') as projects:
        data = projects.read()
        projects = json.loads(data)
    return templates.TemplateResponse('index.html', {"request": request, "cards": projects, **settings})


@app.get('/portfolio/{id}/')
def card(request: Request, id: int):
    with open('projects.json', encoding='utf8') as projects:
        data = projects.read()
        projects = json.loads(data)

    if id < 0 or id >= len(projects):
        return templates.TemplateResponse('404.html', {"request": request})

    return templates.TemplateResponse('card.html', {"request": request, "card": projects[id]})


@app.exception_handler(404)
def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return templates.TemplateResponse('404.html', {"request": request})


if __name__ == "__main__":
    uvicorn.run(
        "main:app"
    )