from pydantic import BaseModel


class PostCreateSchema(BaseModel):
    title: str
    body: str

    # class Config:
    #     orm_mode = True


class PostEditSchema(BaseModel):
    title: str
    body: str