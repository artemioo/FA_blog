from fastapi import APIRouter, Form, Depends, HTTPException, Path
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates


from app.utils import valid_schema_data_or_error
from . import models

from .schemas import PostCreateSchema, PostEditSchema
from .models import Post
from app.db.db_session import get_db
from app.shortcuts import get_object_or_404

templates = Jinja2Templates(directory='app/templates') #указываем путь к папке
router = APIRouter(
    prefix='/posts',
    tags=["posts"])


@router.get('/create', response_class=HTMLResponse)
def post_create_get_view(request: Request):
    return templates.TemplateResponse('/posts/create.html', {'request': request})


@router.post('/create', response_class=HTMLResponse)
def post_create_post_view(request: Request, db = Depends(get_db),
                title: str = Form(...),
                body: str = Form(...)):
    raw_data = {
        'title': title,
        'body': body
    }
    data, errors = valid_schema_data_or_error(raw_data, PostCreateSchema)
    context = {
        'data': data,
        'errors': errors,
    }
    # if len(errors) > 0:
    #     raise HTTPException("Не тот тип")
    post = Post(title=data['title'], body=data['body'])
    db.add(post)
    db.commit()
    return RedirectResponse(url='/', status_code=302)


@router.get('/{id}', response_class=HTMLResponse)
def post_read_view(request: Request,
                   id: int = Path(title='The ID of the post to get'),
                   db: Session = Depends(get_db)):
    post = get_object_or_404(request, id, Post, db)
    return templates.TemplateResponse('/posts/detail.html', {'request': request, 'post': post})


@router.get('{id}/edit', response_class=HTMLResponse)
def post_edit_get_view(request: Request,
                         db: Session = Depends(get_db),
                         id: int = Path(title='The ID of the post to edit')):
    post = get_object_or_404(request, id, Post, db)
    return templates.TemplateResponse('/posts/edit.html', {'request': request, 'object': post})


@router.post('/{id}/edit', response_class=HTMLResponse)
def post_edit_post_view(request: Request,
                     db: Session = Depends(get_db),
                     id: int = Path(title='The ID of the post to edit'),
                     title: str = Form(),
                     body: str = Form()):
    post = get_object_or_404(request, id, Post, db)
    raw_data = {
        'title': title,
        'body': body
    }
    data, errors = valid_schema_data_or_error(raw_data, PostEditSchema)

    post.title = data['title']
    post.body = data['body']
    db.commit()
    return RedirectResponse(url='/posts/', status_code=302)


@router.post('/{id}/delete', response_class=HTMLResponse)
def post_delete_view(request: Request,
                     db: Session = Depends(get_db),
                     id: int = Path(title='The ID of the post to edit')):
    post = get_object_or_404(request, id, Post, db)
    db.delete(post)
    db.commit()
    return RedirectResponse(url='/', status_code=302)