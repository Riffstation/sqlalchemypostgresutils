from .base import get_db_conf, Base, Session
from sqlalchemy.ext.declarative import declared_attr
from .schema import SurrogatePK

class BaseManager(object):
    """
    Base manager, every model will have this common manager
    that allows us to perform database common operations
    """
    def __init__(self, model):
        self._model = model

    def filter_by(self, order_by='id', limit=500, offset=0, **kwargs):
        return self.session.query(
            self._model
            ).filter_by(
                **kwargs
            ).order_by(order_by).limit(limit).offset(offset)

    def get(self, id):
        return self.session.query(self._model).get(id)


    def count(self):
        result = Session.execute(
            'SELECT count(id) from {}'.format(self._model.__table__.name)
        )

        r = result.fetchone()
        if len(r) > 0:
            return r[0]
        else:
            return 0



class BaseModel(Base, SurrogatePK):
    """Abstract base model, contains common field and methods for all models
    """
    __abstract__ = True

    def __init__(self, **kwargs):
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
        dbconf = get_db_conf()
        try:
            if not hasattr(self, 'session'):
                self.session = get_session(dbconf.SQLALCHEMY_DATABASE_URI)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error

    def add(self):
        Session.add(self)
        Session.flush()

    def delete(self):
        try:
            if not hasattr(self, 'session'):
                dbconf = get_db_conf()
                self.session = get_session(dbconf.SQLALCHEMY_DATABASE_URI)

            self.session.delete(self)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error
