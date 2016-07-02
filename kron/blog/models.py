from datetime import datetime

from flask import url_for

from kron import db, uniqid


tags_posts = db.Table(
    "tags_posts",
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"))
)


class Post(db.Model):
    __tablename__ = "posts"
    __tableid__ = uniqid()
    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(8), unique=True, index=True)
    title = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime)
    body = db.Column(db.UnicodeText)
    tags = db.relationship(
        "Tag", secondary=tags_posts,
        backref=db.backref("posts", lazy="joined")
    )

    def __init__(self, title, body):
        db.Model.__init__(self)
        self.id = Post.__tableid__ + uniqid()
        self.title = title
        self.body = body

    def to_dict(self):
        rv = dict(
            id=self.id,
            title=self.title,
            timestamp=self.timestamp,
            body=self.body
        )
        if self.tags:
            rv["tags"] = [dict(
                name=t.name,
                url=t.get_url()
            ) for t in self.tags]
        return rv

    def get_url(self, full=False):
        return url_for("blog_api.get_post", id=self.id, _external=full)

    def __repr__(self):
        return "<Post {id}>".format(id=self.id)


class Tag(db.Model):
    __tablename__ = "tags"
    __tableid__ = uniqid()
    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(8), unique=True, index=True)
    name = db.Column(db.String(64), unique=True, index=True)

    def __init__(self, name):
        db.Model.__init__(self)
        self.id = Tag.__tableid__ + uniqid()
        self.name = name

    def to_dict(self, posts=False):
        rv = dict(
            id=self.id,
            name=self.name
        )
        if self.posts:
            rv["posts"] = [dict(
                id=p.id,
                url=p.get_url()
            ) for p in self.posts]
        return rv

    def get_url(self, full=False):
        return url_for("blog_api.get_tag", name=self.name, _external=full)

    def __repr__(self):
        return "<Tag {name}>".format(name=self.name)
