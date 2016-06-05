from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """Abstract base model, contiains common field and methods for all models
    """
    __abstract__ = True

    def __init__(self, **kwargs):
        dbconf = get_db_conf()
        self.session = get_session(dbconf.SQLALCHEMY_DATABASE_URI)
        for name, value in kwargs.items():
            setattr(self, name, value)

    def close_session(self):
        if self.session:
            self.session.close_all()

    id = Column(Integer, primary_key=True)

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
