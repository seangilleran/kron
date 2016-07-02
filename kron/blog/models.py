import json
from datetime import datetime

from flask import url_for

from kron import db


tags_posts = db.Table(
    "tags_posts",
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"))
)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime)
    body = db.Column(db.Text)
    tags = db.relationship(
        "Tag", secondary=tags_posts,
        backref=db.backref("posts", lazy="joined")
    )

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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)

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
