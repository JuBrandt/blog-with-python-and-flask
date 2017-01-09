import re

from flask import render_template, redirect, url_for, flash
from app import app, db, lm
from .models import Blog, Admin
from sqlalchemy import desc
from datetime import datetime
from .forms import BlogForm, LoginForm
from config import SNIPPET_LENGTH, PER_PAGE, ARCHIVE_PER_PAGE
from flask_login import login_user, logout_user, login_required


def make_snippet(text):
    # Makes a snippet of text / features for use on the index page

    lines = text[:SNIPPET_LENGTH].split('\n')
    can_have_image = True
    snippet = []

    for line in lines:
        # Check for 0 length and add newline if found -- for Markdown
        if len(line) > 0:
            # If line starts with '!' most likely an image
            if line[0] == '!':
                # Restrict the amount of images on the index page
                if can_have_image:
                    snippet.append(line)
                    can_have_image = False
            else:
                snippet.append('\n')
        else:
            snippet.append(line)

    # Remove broken html
    if snippet[-1].count('>') % 2 != 0:
        del snippet[-1]

    snippet = '\n'.join(snippet)

    # Decide whether to add '...' if incomplete sentence
    if snippet[-1] != '.':
        snippet += '...'
    return snippet


def make_address(title):
    pattern = re.compile('[a-z0-9A-Z]+')
    address = ' '.join(re.findall(pattern, title)).replace(' ', '-').lower()
    return address


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    posts = Blog.query.order_by(desc(Blog.blog_date)).paginate(page, PER_PAGE, False) # noqa
    return render_template('index.html',
                           title='Home',
                           posts=posts)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = BlogForm()
    if form.validate_on_submit():
        blog_title = form.blog_title.data
        blog_body = form.blog_body.data
        blog_date = datetime.utcnow()
        blog_address = blog_title.replace(' ', '-')
        blog_snippet = make_snippet(blog_body)
        b = Blog(blog_title=blog_title,
                 blog_body=blog_body,
                 blog_date=blog_date,
                 blog_address=blog_address,
                 blog_snippet=blog_snippet)
        db.session.add(b)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('create.html', title='Create', form=form)


@app.route('/edit/<slug>', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('success'))
    return render_template('edit.html',
                           title='Edit - ' + post.blog_title,
                           form=form,
                           post=post)


@app.route('/success')
def success():
    # For admin use to indicate successful post
    return render_template('success.html', title='Success')


@app.route('/failure')
def failure():
    # For admin use to indicate unsuccessful post
    return render_template('failure.html', title='Failure')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        admin = Admin.query.filter_by(login=login).first()
        if admin is None:
            flash('Incorrect login!')
            return redirect(url_for('failure'))
        if password == admin.password:
            login_user(admin)
            return redirect(url_for('admin'))
    return render_template('login.html',  title='Login', form=form)


@lm.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html', title='Admin')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html', title='500'), 500


@app.route('/detail/<slug>')
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


@app.route('/archive')
@app.route('/archive/<int:page>')
def archive(page=1):
    posts = Blog.query.order_by(desc(Blog.blog_date)).paginate(page, ARCHIVE_PER_PAGE, False) # noqa
    return render_template('archive.html', title='Archive', posts=posts)


@app.route('/anout')
def about():
    return render_template('about.html', title='About')
