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
    html = db.Column(db.Text)
    tags = db.relationship(
        "Tag", secondary=tags_posts,
        backref=db.backref("posts", lazy="joined")
    )

    @staticmethod
    def from_dict(data):
        now = datetime.utcnow().strftime("%m %d %Y")
        post = Post(
            title=data.get("title", ""),
            timestamp=datetime.strptime(
                data.get("timestamp", now), "%m %d %Y"),
            body=data.get("body", "")
        )
        if data.get("tags"):
            post.tags.extend([
                Tag.query.filter_by(id=t["id"]).first() for
                t in data["tags"]
            ])
        return post

    def to_dict(self):
        data = {
            "id": self.id,
            "title": self.title,
            "body": self.body,
        }
        if self.timestamp:
            data.update(timestamp=self.timestamp.strftime("%m %d %Y"))
        if self.html:
            data.update(html=self.html)
        if self.tags:
            data.update(tags=[{
                "id": t.id,
                "url": t.get_url()
            } for t in self.tags])
        return data

    @staticmethod
    def all_to_dict():
        return {
            "posts": [p.to_dict() for p in Post.query.all()]
        }

    def get_url(self, full=False):
        return url_for("blog.get_post", id=self.id, _external=full)

    def __repr__(self):
        return "<Post {id}>".format(id=self.id)


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    @staticmethod
    def from_dict(data):
        tag = Tag(name=data.get("Name"))
        if data.get("posts"):
            tag.posts.extend([
                Post.query.filter_by(id=p["id"]).first() for
                p in data["posts"]
            ])
        return tag

    def to_dict(self, posts=False):
        data = {
            "id": self.id,
            "name": self.name,
            "url": self.get_url()
        }
        if self.posts:
            data.update(posts=[{
                "id": p.id,
                "url": p.get_url(),
            } for p in self.posts])
        return data

    @staticmethod
    def all_to_dict():
        return {
            "tags": [t.to_dict() for t in Tag.query.all()]
        }

    def get_url(self, full=False):
        return url_for("blog.get_tag", id=self.id, _external=full)

    def __repr__(self):
        return "<Tag {name}>".format(name=self.name)
