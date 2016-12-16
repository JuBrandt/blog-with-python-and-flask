from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown

app = Flask(__name__)
Markdown(app)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
