from fastapi import APIRouter
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from fastapi import APIRouter, Form, Depends, HTTPException, Path
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates


from app.utils import valid_schema_data_or_error
from .models import User
from .schemas import UserSignUpSchema

from app.db.db_session import get_db
from app.shortcuts import get_object_or_404


templates = Jinja2Templates(directory='app/templates') #указываем путь к папке
router = APIRouter(
    prefix='/users',
    tags=["users"])


@router.get('/signup', response_class=HTMLResponse)
def create_user_get_view(request: Request):
    return templates.TemplateResponse('/users/signup.html', {'request': request, })


@router.post('/signup', response_class=HTMLResponse)
def create_user_post_view(request: Request,
                          db: Session = Depends(get_db),
                          username: str = Form(),
                          email: str = Form(),
                          first_name: str = Form(),
                          last_name: str = Form(),
                          bio: str = Form(),
                          password: str = Form(),
                          password_confirm: str = Form(),
                          ):
    raw_data = {
        'username': username,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'bio': bio,
        'password': password,
        'password_confirm': password_confirm
    }
    data, errors = valid_schema_data_or_error(raw_data, UserSignUpSchema)
    User.create_user(data['email'], data['password'], data['username'], db=db,)
    if len(errors) > 0:
        pass
    return RedirectResponse(url='/posts')