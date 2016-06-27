from flask import current_app

from kron import db


tags = db.Table(
    "tags",
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"))
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime)
    body = db.Column(db.Text)
    html = db.Column(db.Text)
    tags = db.relationship(
        "Tag", secondary=tags,
        backref=db.backref("posts", lazy="dynamic")
    )

    def __repr__(self):
        return "<Post {id}>".format(id=self.id)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return "<Tag {name}>".format(name=self.name)
