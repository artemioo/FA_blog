from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates


from app.utils import valid_schema_data_or_error

from .schemas import PostCreateSchema
from .models import Post



templates = Jinja2Templates(directory='app/templates') #указываем путь к папке
router = APIRouter(tags=["posts"])


@router.get('/posts', response_class=HTMLResponse)
def post_create_get_view(request: Request):
    return templates.TemplateResponse('/posts/create.html', {'request': request})


@router.post('/posts', response_class=HTMLResponse)
def post_create_post_view(request: Request,
                title: str = Form(...),
                body: str = Form(...)):
    raw_data = {
        'title': title,
        'body': body
    }
    print(raw_data)
    data, errors = valid_schema_data_or_error(raw_data, PostCreateSchema)
    context = {
        'data': data,
        'errors': errors,
    }
    print(context)
    # post = Post(title=context[data][title])
    return RedirectResponse(url='/')