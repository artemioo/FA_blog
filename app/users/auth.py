import datetime

import jwt
from fastapi import Depends
from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import JWTStrategy
from dotenv import load_dotenv
from fastapi_users.authentication import AuthenticationBackend, JWTStrategy
import os

from jose import ExpiredSignatureError
from sqlalchemy.orm import Session

from app.db.db_session import get_db
from app.users.models import User

load_dotenv()
cookie_transport = CookieTransport(cookie_name='FA_blog', cookie_max_age=3600)

JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM')


def authenticate(username, password, db):
    # step 1
    user_obj = db.query(User).filter(User.username == username).first()
    if not user_obj.verify_password(password):
        return None
    # if user_obj is None:
    #     raise UserDoesntExists
    return user_obj


def login(user_obj, expires=1200):
    # step 2
    raw_data = {
        "user_id": f'{user_obj.user_id}',
        'role': "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta
        (seconds=expires)
    }
    return jwt.encode(raw_data, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_user_id(token):
    # step 3
    data = {}
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except ExpiredSignatureError as e:
        print(e)
    except:
        pass
    if 'user_id' not in data:
        return None
    return data