# sqlalchemypostgresutils
Simple library that uses  [SQLAlchemy](http://www.sqlalchemy.org/) to access postgresql databases.

## What this project is about?

Sqlalchemy is a great library that supports different database servers. Here in riffstation.com
we use postgresql across several microservices, anytime that we need to create a new microservice
we need to bootstrap very similar common code.
This library wants to concentrate all this database logic  in one common place. Feel free to use it and
extendent it. We are willing to hear about your suggestions and improvements.


## Executing test

In order to run test, a postgresql database is required, easiest way to provide a postgresql installation
is by using a vagrant instance, below steps required to execute unit tests:

```
   cd test
   vagrant up
   vagrant ssh
   cd /src/test
   python3 run_test.py
```

## Usage


### Connection Configuration

You need to specify  a [postgresql url before start using this library:] (http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls)

```
from pgsqlutils.base import get_db_conf, init_db_conn

# getting configuration object
pg_conf = get_db_conf()

# updating postgresql url
pg_conf.DATABASE_URI = 'postgresql://ds:dsps@localhost:5432/ds'

# init connection, just have to do it once
init_db_conn()
```

### A simple models example

```

from pgsqlutils.orm import BaseModel

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Artist(BaseModel):
    __tablename__ = 'artist'
    name = Column(String(256))
    description = Column(String(256))
    albums = relationship('Album', backref='artist')
    genre_id = Column(Integer, ForeignKey('genre.id'))


class Album(BaseModel):
    __tablename__ = 'album'
    name = Column(String(256))
    description = Column(String(256))
    artist_id = Column(Integer, ForeignKey('artist.id'))


class Genre(BaseModel):
    __tablename__ = 'genre'
    name = Column(String(256))
    description = Column(String(256))

```


### Interacting with the models

```
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


        wall = Album(
            artist_id=pink.id, name='The Wall',
            description='Interesting')
        wall.add()
```



## External Resources

* [SQLAlchemy Website.](http://www.sqlalchemy.org/)

* [Mike Bayer: Building the App - PyCon 2014](https://www.youtube.com/watch?v=5SSC6nU314c)

* [Mike Bayer: Building the App - PyCon 2014 Source code](https://bitbucket.org/zzzeek/pycon2014_atmcraft)
