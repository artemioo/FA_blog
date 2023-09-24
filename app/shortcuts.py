from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse


def get_object_or_404(request: Request, id: int, model_class, db: Session):
    obj = db.query(model_class).filter(model_class.id == id).first()
    if obj is None:
        raise HTTPException(status_code=404, detail='That object doesn`t exists, Sorry!)')
        # return HTMLResponse(content='That object doesn`t exists, Sorry!)')
    return obj
