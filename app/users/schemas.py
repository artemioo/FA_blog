from pydantic import BaseModel, model_validator, field_validator, root_validator, EmailStr, SecretStr

from app.users import auth
from app.users.models import User


class UserSignUpSchema(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr
    password_confirm: SecretStr
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


class UserLoginSchema(BaseModel):
    username: str
    password: str
    token: str = None

    # @model_validator(mode='after')
    # def validate_user(self):
    #     """
    #      валидирует юзера с помощью других методов и присваивает токен
    #     """
    #     err_msg = 'Incorrect email or password'
    #     username = self.username
    #     password = self.password
    #     if username is None or password is None:
    #         raise ValueError(err_msg)
    #     password = password.get_secret_value()  # SecretStr method, получаем пароль в открытом виде
    #     user_obj = auth.authenticate(username, password)
    #     token = auth.login(user_obj)
    #     return {'session_id': token}