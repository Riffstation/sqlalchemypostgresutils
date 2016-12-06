from pgsqlutils.base import syncdb
from pgsqlutils.types import PasswordHash


class TestPassword(object):
    def setup(self):
        syncdb()

    def test_password_equal(self):
        a = PasswordHash.new('123', 12)
        assert a == '123'
        assert a != '1232'
