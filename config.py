import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret'  # should be unique to app
DEBUG = True

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

PER_PAGE = 3
SNIPPET_LENGTH = 200
ARCHIVE_PER_PAGE = 5
