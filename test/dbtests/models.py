from pgsqlutils.orm import one_to_many, many_to_one, BaseModel

from sqlalchemy import Column, String
from sqlalchemy.orm.collections import attribute_mapped_collection


class Artist(BaseModel):
    __tablename__ = 'artists'
    name = Column(String(256))
    description = Column(String(256))
    albums = one_to_many('Album', backref='artist', lazy="immediate")


class Album(BaseModel):
    __tablename__ = 'albums'
    artist = many_to_one("Artist", lazy="joined", innerjoin=True)
    name = Column(String(256))
    description = Column(String(256))
