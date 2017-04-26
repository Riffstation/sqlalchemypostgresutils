from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import text

from .base import Base
from .exceptions import NotFoundError, InvalidQueryError

Session = None


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

    def get_for_update(self, **kwargs):
        """
        http://docs.sqlalchemy.org/en/latest/orm/query.html?highlight=update#sqlalchemy.orm.query.Query.with_for_update  # noqa
        """
        if not kwargs:
            raise InvalidQueryError(
                "Can not execute a query without parameters")
        obj = Session.query(
            self._model).with_for_update(
                nowait=True, of=self._model).filter_by(**kwargs).first()
        if not obj:
            raise NotFoundError('Object not found')
        return obj

    def get(self, **kwargs):
        if not kwargs:
            raise InvalidQueryError(
                "Can not execute a query without parameters")
        obj = Session.query(self._model).filter_by(**kwargs).first()

        if not obj:
            raise NotFoundError('Object not found')
        return obj

    def count(self):
        result = Session.execute(
            'SELECT count(id) from {}'.format(self._model.__table__.name)
        )

        r = result.fetchone()
        if len(r) > 0:
            return r[0]
        else:
            return 0

    def raw_sql(self, sql, **kwargs):
        return Session.execute(text(sql), kwargs)


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

    def update(self):
        Session.flush()

    def add(self):
        Session.add(self)
        Session.flush()

    def delete(self):
        Session.delete(self)
        Session.flush()
