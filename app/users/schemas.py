from pydantic import BaseModel, model_validator, field_validator
from app.users.models import User


class UserSignUpSchema(BaseModel):
    username: str
    email: str
    password: str
    password_confirm: str
    first_name: str
    last_name: str
    bio: str

    @model_validator(mode='after')
    def passwords_match(self):
        password = self.password
        password_confirm = self.password_confirm
        if password != password_confirm:
            raise ValueError("Passwords do not match")
        return self
