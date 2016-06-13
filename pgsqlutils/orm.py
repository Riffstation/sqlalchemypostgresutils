from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr

from .base import Base, Session


class BaseManager(object):
    """
    Base manager, every model will have this common manager
    that allows us to perform database common operations
    """
    def __init__(self, model):
        self._model = model

    def filter_by(self, order_by='id', limit=500, offset=0, **kwargs):
        return Session.query(
            self._model
            ).filter_by(
                **kwargs
            ).order_by(order_by).limit(limit).offset(offset)

    def get(self, id):
        return Session.query(self._model).get(id)

    def count(self):
        result = Session.execute(
            'SELECT count(id) from {}'.format(self._model.__table__.name)
        )

        r = result.fetchone()
        if len(r) > 0:
            return r[0]
        else:
            return 0


class BaseModel(Base):
    """Abstract base model, contains common field and methods for all models
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)
        for name, value in kwargs.items():
            if not name.startswith('_'):
                setattr(self, name, value)

    @declared_attr
    def objects(cls):
        return BaseManager(cls)

    @classmethod
    def raw_sql(cls, sql, **kwargs):
        return Session.execute(sql, kwargs)

    def update(self):
        Session.flush()

    def add(self):
        Session.add(self)
        Session.flush()

    def delete(self):
        Session.delete(self)
        Session.flush()
