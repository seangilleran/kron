from datetime import datetime
import re

from flask import url_for, current_app
from markdown import markdown
import bleach

from kron import db, uniqid


tags_posts = db.Table(
    "tags_posts",
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"))
)


class Tag(db.Model):
    __tablename__ = "tags"
    __tableid__ = uniqid()
    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    full_name = db.Column(db.String(64), unique=True)

    def __init__(self, name):
        db.Model.__init__(self)
        self.id = Tag.__tableid__ + uniqid()
        self.full_name = name

    @staticmethod
    def on_set_name(target, value, oldvalue, initiator):
        target.name = re.sub("[^A-Za-z]", "_", value).lower()

    def get_url(self, full=False):
        return url_for("blog.get_tag", name=self.name, _external=full)

    def __repr__(self):
        return "<Tag {id}>".format(name=self.id)


db.event.listen(Tag.full_name, "set", Tag.on_set_name)


class Post(db.Model):
    __tablename__ = "posts"
    __tableid__ = uniqid()
    id = db.Column(db.String(8), primary_key=True)
    timestamp = db.Column(db.DateTime)
    title = db.Column(db.String(128), unique=True, index=True)
    full_title = db.Column(db.String(128), unique=True)
    body = db.Column(db.UnicodeText)
    body_html = db.Column(db.UnicodeText)
    tags = db.relationship(
        "Tag", secondary=tags_posts,
        backref=db.backref("posts", lazy="joined")
    )

    def __init__(self, title, body):
        db.Model.__init__(self)
        self.id = Post.__tableid__ + uniqid()
        self.full_title = title
        self.body = body

    @staticmethod
    def on_set_title(target, value, oldvalue, initiator):
        target.title = re.sub("[^A-Za-z]", "_", value).lower()

    @staticmethod
    def on_set_body(target, value, oldvalue, initiator):
        allowed_tags = current_app.config.get("ALLOWED_HTML_TAGS")
        html = markdown(value, output_format="html")
        target.body_html = bleach.linkify(
            bleach.clean(html, tags=allowed_tags, strip=True))

    def get_url(self, full=False):
        return url_for("blog.get_post", title=self.title, _external=full)

    def __repr__(self):
        return "<Post {id}>".format(id=self.id)


db.event.listen(Post.full_title, "set", Post.on_set_title)
db.event.listen(Post.body, "set", Post.on_set_body)
