from pydantic import BaseModel


class PostCreateSchema(BaseModel):
    id: int
    title: str
    body: str

    # class Config:
    #     orm_mode = True