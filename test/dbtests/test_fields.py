from pgsqlutils.base import syncdb, Session
from pgsqlutils.types import Password


import bcrypt


class TestPassword(object):
    def setup(self):
        syncdb()

    def test_password_equal(self):
        salt = bcrypt.gensalt(4)
        assert Password('123', salt=salt) == Password('123', salt=salt)

    def test_password_equal_salt_different(self):
        p1 = Password('123', salt=bcrypt.gensalt(4))
        p2 = Password('123', salt=bcrypt.gensalt(4))
        assert p1 != p2

    def teardown(self):
        Session.rollback()
        Session.close()
