from pgsqlutils.base import init_db_conn, syncdb, Session
from .models import Artist, Album, Genre


class TestDB(object):
    def setup(self):
        init_db_conn()

    def test_connection_open(self):
        """
        checks if connection is open
        """
        result = Session.execute('SELECT 19;')
        assert result.fetchone()[0] == 19
        Session.close()


class TestCaseModel(object):
    def setup(self):
        syncdb()

    def test_simple_insert(self):
        syncdb()
        assert 0 == Artist.objects.count()
        artist = Artist()
        artist.add()
        assert 1 == Artist.objects.count()
        artist2 = Artist()
        artist2.add()
        assert 2 == Artist.objects.count()

    def test_relationships(self):
        rock = Genre(name='Rock', description='rock yeah!!!')
        rock.add()
        pink = Artist(
            genre_id=rock.id, name='Pink Floyd', description='Awsome')
        pink.add()
        dark = Album(
            artist_id=pink.id, name='Dark side of the moon',
            description='Interesting')
        dark.add()

        rolling = Artist(
            genre_id=rock.id, name='Rolling Stones', description='Acceptable')

        rolling.add()

        hits = Album(
            artist_id=rolling.id, name='Greatest hits',
            description='Interesting')
        hits.add()

        assert 2 == Album.objects.count()

        wall = Album(
            artist_id=pink.id, name='The Wall',
            description='Interesting')
        wall.add()
        assert 2 == len(pink.albums)
        assert 2 == len(Artist.objects.filter_by(genre_id=rock.id)[:])

    def teardown(self):
        Session.rollback()
        Session.close()
