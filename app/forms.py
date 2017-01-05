from flask_wtf import Form
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import DataRequired


class BlogForm(Form):
    blog_title = StringField('blog_title', validators=[DataRequired()])
    blog_body = TextAreaField('blog_body')


class LoginForm(Form):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
