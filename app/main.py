from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.posts.router import router as posts_router
from .db.db_session import get_db

from .posts.models import Post

app = FastAPI()

templates = Jinja2Templates(directory='app/templates') #указываем путь к папке
app.mount('/static', StaticFiles(directory="app/static"), name='static')
app.include_router(posts_router)


@app.get('/', response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return templates.TemplateResponse('/base.html', {'request': request, "posts": posts})
