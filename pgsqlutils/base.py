from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from .schema import References

# Alex Martelli's 'Borg'
class DBBorg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state

class DBConf(DBBorg):
    pass

conf = DBConf()

def get_db_conf():
    return conf


class DBConnection(object):
    """
    http://docs.sqlalchemy.org/en/latest/core/connections.html
    """
    def __init__(self):
        engine = create_engine(conf.DATABASE_URI)
        self.conn = engine.connect()
        self.transaction = self.conn.begin()
        sm = sessionmaker(bind=self.conn)
        self.session = scoped_session(sm)

    def rollback(self):
        self.transaction.rollback()

    def close(self):
        self.session.close()
        self.conn.close()


class Base(References):
    pass

Base = declarative_base(cls=Base)

# establish a constraint naming convention.
# see http://docs.sqlalchemy.org/en/latest/core/constraints.html#configuring-constraint-naming-conventions
#
Base.metadata.naming_convention = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ix": "ix_%(table_name)s_%(column_0_name)s"
}
