from flask import render_template, redirect, url_for
from app import app, db, freezer
from .models import Blog
from sqlalchemy import desc
from datetime import datetime
from .forms import BlogForm
from config import PER_PAGE, ARCHIVE_PER_PAGE
from .helpers import make_snippet, make_address


@app.route('/')
@app.route('/index/<int:page>/')
def index(page=1):
    posts = Blog.query.order_by(desc(Blog.blog_date)).paginate(page, PER_PAGE, False) # noqa
    return render_template('index.html',
                           title='Home',
                           posts=posts)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    form = BlogForm()
    if form.validate_on_submit():
        blog_title = form.blog_title.data
        blog_body = form.blog_body.data
        blog_date = datetime.utcnow()
        blog_address = make_address(blog_title)
        blog_snippet = make_snippet(blog_body)
        b = Blog(blog_title=blog_title,
                 blog_body=blog_body,
                 blog_date=blog_date,
                 blog_address=blog_address,
                 blog_snippet=blog_snippet)
        db.session.add(b)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html', title='Create', form=form)


@app.route('/edit/<slug>/', methods=['GET', 'POST'])
def edit(slug):
    # For editing existing blog posts

    post = Blog.query.filter_by(blog_address=slug).first()
    form = BlogForm()
    if form.validate_on_submit():
        post.blog_title = form.blog_title.data
        post.blog_body = form.blog_body.data
        post.blog_address = make_address(post.blog_title)
        post.blog_snippet = make_snippet(post.blog_body)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html',
                           title='Edit - ' + post.blog_title,
                           form=form,
                           post=post)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', title='500'), 500


@app.route('/detail/<slug>/')
def detail(slug):
    # For individual blog post
    post = Blog.query.filter_by(blog_address=slug).first()
    next_address = False
    previous_address = False
    if post:
        next_post = Blog.query.filter_by(id=post.id + 1).first()
        previous_post = Blog.query.filter_by(id=post.id - 1).first()
        if next_post:
            next_address = next_post.blog_address
        if previous_post:
            previous_address = previous_post.blog_address
        return render_template('detail.html',
                               title=post.blog_title,
                               post=post,
                               next_address=next_address,
                               previous_address=previous_address)
    return render_template('404.html', title='404'), 404


@app.route('/archive/')
@app.route('/archive/<int:page>/')
def archive(page=1):
    posts = Blog.query.order_by(desc(Blog.blog_date)).paginate(page, ARCHIVE_PER_PAGE, False) # noqa
    return render_template('archive.html', title='Archive', posts=posts)


@app.route('/about/')
def about():
    return render_template('about.html', title='About')


@app.route('/404.html')
def generate_404():
    return render_template('404.html', title='404')


@app.route('/500.html')
def generate_500():
    return render_template('500.html', title='500')


@freezer.register_generator
def error_404():
    yield '/404.html'


@freezer.register_generator
def error_500():
    yield '/500.html'
