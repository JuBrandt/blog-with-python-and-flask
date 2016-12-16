from flask import render_template, redirect, url_for, session
from app import app, db
from .models import Blog
from sqlalchemy import desc
from datetime import datetime
from .forms import BlogForm
from config import SNIPPET_LENGTH, PER_PAGE

@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    posts = Blog.query.order_by(desc(Blog.blog_date)).paginate(page, PER_PAGE, False)
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
        if len(blog_body) > SNIPPET_LENGTH:
            blog_snippet = blog_body[:SNIPPET_LENGTH] + '...'
        b = Blog(blog_title=blog_title,
                blog_body=blog_body,
                blog_date=blog_date,
                blog_address=blog_address,
                blog_snippet=blog_snippet)
        db.session.add(b)
        db.session.commit()
        #return render_template('success.html', title='Success')
        return redirect(url_for('success'))
    return render_template('create.html', title='Create', form=form)

@app.route('/success')
def success():
    return render_template('success.html', title='Success')
