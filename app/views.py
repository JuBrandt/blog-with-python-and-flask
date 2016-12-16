from flask import render_template, redirect, url_for
from app import app, db
from .models import Blog
from sqlalchemy import desc
from datetime import datetime
from .forms import BlogForm

@app.route('/')
@app.route('/index')
def index():
    posts = Blog.query.order_by(desc(Blog.blog_date)).limit(10).all()
    return render_template('index.html',
                            title='Home',
                            posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = BlogForm()
    if form.validate_on_submit():
        blog_title = form.blog_title.data
        blog_body = form.blog_body.data
        blog_date = datetime.utcnow()
        blog_address = blog_title.replace(' ', '-')
        b = Blog(blog_title=blog_title, blog_body=blog_body, blog_date=blog_date, blog_address=blog_address)
        db.session.add(b)
        db.session.commit()
        #return render_template('success.html', title='Success')
        return redirect(url_for('success'))
    return render_template('create.html', title='Create', form=form)

@app.route('/success')
def success():
    return render_template('success.html', title='Success')
