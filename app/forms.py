from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class BlogForm(Form):
    """For creating and editing blog post."""
    blog_title = StringField('blog_title', validators=[DataRequired()])
    blog_body = TextAreaField('blog_body')
