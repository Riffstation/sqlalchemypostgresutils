from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
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


engine = None

Session = scoped_session(sessionmaker())


def init_db_conn():
    """
    Engine and session maker should be global, so there will be attached
    to Borg configuration object
    """
    conf = get_db_conf()
    global engine
    engine = create_engine(conf.DATABASE_URI)
    Session.configure(bind=engine)



def syncdb():
    """
    Create tables if they don't exist
    """
    Base.metadata.create_all(engine)


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
