from starlette.requests import Request

from app.users.auth import verify_user_id
from app.users.models import User


def get_user_info(request: Request, token, db):
    data = verify_user_id(token)
    if data:
        data = db.query(User).filter(User.user_id == data['user_id']).first()
    return data