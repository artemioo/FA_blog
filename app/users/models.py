from sqlalchemy import Column, DateTime, Integer, Text

from sqlalchemy.sql import func
from app.db.base_class import Base
from app.users import security
from app.users.exceptions import UserHasAccountException, InvalidEmailException
from app.users.validators import _validate_email_util


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(Text, primary_key=True, index=True)
    email = Column(Text, primary_key=True)
    password = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    bio = Column(Text)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    # author_id = Column(Integer, ForeignKey('author.id'))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'User(email={self.email}, user_id={self.user_id})'

    def set_password(self, pw, commit=False):
        pw_hash = security.generate_hash(pw)
        self.password = pw_hash
        if commit:
            self.save()
        return True

    def verify_password(self, pw_str):
        pw_hash = self.password
        verified, _ = security.verify_hash(pw_hash, pw_str)
        return verified

    @staticmethod
    def create_user(email, password=None, username=None, first_name=None, last_name=None, bio=None, db=None):
        if db.query(User).filter(User.email == email).count():
            raise UserHasAccountException('User already has account')
        valid, msg, email = _validate_email_util(email)
        if not valid:
            raise InvalidEmailException("Invalid email: {msg}")
        obj = User(email=email, username=username, first_name=first_name, last_name=last_name, bio=bio)
        obj.set_password(password)
        db.add(obj)
        db.commit()
        return obj
