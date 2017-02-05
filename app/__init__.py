from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from flask_frozen import Freezer

app = Flask(__name__)
Markdown(app)
app.config.from_object('config')
db = SQLAlchemy(app)

freezer = Freezer(app)

from app import views, models # noqa
