from pgsqlutils.orm import BaseModel

from sqlalchemy import Column, String


class Artist(BaseModel):
    __tablename__ = 'artists'
    name = Column(String(256))
    description = Column(String(256))


class Album(BaseModel):
    name = Column(String(256))
    description = Column(String(256))
