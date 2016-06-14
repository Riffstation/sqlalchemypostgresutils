from setuptools import setup
setup(
    name='sqlalchemypostgresutils',
    version='1.0.0',
    description='Sqlalchemy and Postgresql Utilities',
    packages=['pgsqlutils'],
    author='Manuel Ignacio Franco Galeano',
    author_email='maigfrga@gmail.com',
    install_requires=[
        'SQLAlchemy>=1.0'],
)
