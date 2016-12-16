from app import db

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120), index=True, unique=True)
    blog_body = db.Column(db.Text, index=True)
    blog_date = db.Column(db.DateTime)
    blog_address = db.Column(db.String(120), index=True, unique=True)
    blog_snippet = db.Column(db.Text, index=True)

    def __repr__(self):
        return self.blog_title
