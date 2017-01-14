import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'secret'  # should be unique to app
DEBUG = True  # should change to False before deployment

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

PER_PAGE = 5  # number of posts on index page
SNIPPET_LENGTH = 200   # character length for snippet for index page
ARCHIVE_PER_PAGE = 20  # number of archive titles on archive page
