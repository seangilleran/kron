from datetime import datetime

from flask import url_for

from kron import db, is_ok, ModelEventListeners
from kron.exceptions import APIInvalidUsage


tags_posts = db.Table(
    "tags_posts",
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"))
)


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __init__(self, name):
        db.Model.__init__(self)
        self.name = name

    @staticmethod
    def from_dict(data):
        data = data.get("tag")
        if not is_ok(data):
            raise APIInvalidUsage("Missing data: tag")
        if not is_ok(data.get("name")):
            raise APIInvalidUsage("Missing data: tag.name")
        return Tag(name=data["name"])

    def update_from_dict(self, data):
        data = data.get("tag")
        if not is_ok(data):
            raise APIInvalidUsage("Missing data: tag")
        if is_ok(data.get("name")):
            self.name == data["name"]

    def to_dict(self):
        rv = dict(tag=dict(
            id=self.id, name=self.name,
            posts=[dict(url=p.get_url()) for p in self.posts]
        ))
        for key in list(rv["tag"]):
            if not is_ok(rv["tag"][key]):
                rv["tag"].pop(key, None)
        return rv

    def get_url(self, full=False):
        return url_for("blog.get_tag", id=self.id, _external=full)

    def __repr__(self):
        return "<Tag {id}>".format(id=self.id)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    title = db.Column(db.String(128), unique=True, index=True)
    body = db.Column(db.UnicodeText)
    tags = db.relationship(
        "Tag", secondary=tags_posts, backref="posts")

    def __init__(self, title, body):
        db.Model.__init__(self)
        self.timestamp = datetime.utcnow()
        self.title = title
        self.body = body

    @staticmethod
    def from_dict(data):
        data = data["post"]
        if not is_ok(data):
            raise APIInvalidUsage("Missing data: post")
        if not is_ok(data.get("title")):
            raise APIInvalidUsage("Missing data: post.title")
        if not is_ok(data.get("body")):
            raise APIInvalidUsage("Missing data: post.body")
        return Post(
            title=data["title"], body=data["body"]
        )

    def update_from_dict(self, data):
        data = data["post"]
        if not is_ok(data):
            raise APIInvalidUsage("Missing data: post")
        if is_ok(data.get("title")):
            self.title = data["title"]
        if is_ok(data.get("body")):
            self.body = data["body"]

    def to_dict(self):
        rv = dict(post=dict(
            id=self.id, title=self.title,
            body=self.body,
            timestamp=datetime.strftime(
                self.timestamp, '%b %d %Y %I:%M%p'),
            tags=[dict(url=t.get_url()) for t in self.tags]
        ))
        for key in list(rv["post"]):
            if not is_ok(rv["post"][key]):
                rv["post"].pop(key, None)
        return rv

    def get_url(self, full=False):
        return url_for("blog.get_post", id=self.id, _external=full)

    def __repr__(self):
        return "<Post {id}>".format(id=self.id)
