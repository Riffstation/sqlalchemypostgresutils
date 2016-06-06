from pgsqlutils.base import get_db_conf, DBConnection
from pgsqlutils.orm import BaseModel
from .models import Artist


class TestConfig(object):

    def test_db_conf(self):
        """
        Check that all instances of config have same configuration
        values
        """
        conf = get_db_conf()
        assert hasattr(conf, 'DATABASE_URI') == False
        conf.DATABASE_URI = 'postgresql://ds:dsps@localhost:5432/ds'
        conf2 = get_db_conf()
        assert hasattr(conf2, 'DATABASE_URI')
        assert conf.DATABASE_URI == conf2.DATABASE_URI


class TestDB(object):
    def setup(self):
        self.conf = get_db_conf()
        self.conf.DATABASE_URI = 'postgresql://ds:dsps@localhost:5432/ds'

    def test_connection_open(self):
        """
        checks if connection is open
        """
        conn = DBConnection()
        result = conn.session.execute('SELECT 19;')
        assert result.fetchone()[0] == 19
        conn.close()


class TestCaseModel(object):
    def setup(self):
        self.conf = get_db_conf()
        self.conf.DATABASE_URI = 'postgresql://ds:dsps@localhost:5432/ds'
        self.conn = DBConnection()
        self.conn.syncdb()

    def test_simple_insert(self):
        print('a')

    def teardown(self):
        self.conn.rollback()
        self.conn.close()
