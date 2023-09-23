from sqlalchemy import Column, DateTime, Integer, String, Text

from sqlalchemy.sql import func
from app.db.base_class import Base


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(Text)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    # tags
    # author_id = Column(Integer, ForeignKey('author.id'))

