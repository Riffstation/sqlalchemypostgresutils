from .base import Base, DBConnection
from .schema import SurrogatePK

class BaseManager(object):
    """
    Base manager, every model will have this common manager
    that allows us to perform database common operations
    """
    def __init__(self, model, session):
        self._model = model
        self.session = session

    def filter_by(self, order_by='id', limit=500, offset=0, **kwargs):
        return self.session.query(
            self._model
            ).filter_by(
                **kwargs
            ).order_by(order_by).limit(limit).offset(offset)

    def get(self, id):
        return self.session.query(self._model).get(id)

    def get_authentication(self, user_id):
        try:
            return self.session.query(
                self._model).filter_by(user_id=user_id).one()
        except exc.SQLAlchemyError:
            return None

    def get_usersongs(self, user_id):
        try:
            return self.session.query(
                self._model).filter_by(user_id=user_id).all()
        except exc.SQLAlchemyError:
            return None

    def get_usersong_count(self, user_id):
        try:
            return self.session.query(
                self._model).filter_by(user_id=user_id).count()
        except exc.SQLAlchemyError:
            return None

    def count(self):
        result = self.session.execute(
            'SELECT count(id) from {}'.format(self._model.__table__.name)
        )
        r = result.fetchone()
        if len(r) > 0:
            return r[0]
        else:
            return 0

    def all(self):
        results = self.session.query(self._model).order_by('id').all()
        data_array = []
        for result in results:
            # remove unnecessary k/v pair that is not JSON serializable
            result.__dict__.pop('_sa_instance_state', None)
            data_array.append(result.__dict__)
        return data_array




class BaseModel(Base, SurrogatePK):
    """Abstract base model, contains common field and methods for all models
    """
    __abstract__ = True

    def __init__(self, **kwargs):
        self._conn = DBConnection()
        for name, value in kwargs.items():
            if not name.startswith('_'):
                setattr(self, name, value)

    def close_session(self):
        if self.session:
            self.session.close_all()


    @classmethod
    def objects(cls):
        dbconf = get_db_conf()
        session = get_session(dbconf.SQLALCHEMY_DATABASE_URI)
        return BaseManager(cls, session)

    @classmethod
    def raw_sql(cls, sql, **kwargs):
        if not hasattr(cls, 'session'):
            cls.session = get_session()
        return cls.session.execute(sql, kwargs)

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
        dbconf = get_db_conf()
        try:
            if not hasattr(self, 'session'):
                self.session = get_session(dbconf.SQLALCHEMY_DATABASE_URI)

            self.session.add(self)
            self.session.commit()
        except Exception as error:
            self.session.rollback()
            raise error

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
