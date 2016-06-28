import json

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

    def __repr__(self):
        return "<Post {id}>".format(id=self.id)

    def to_json(self):
        data = {
            "id": self.id,
            "title": self.title,
            "timestamp": self.timestamp,
            "body": self.body,
            "html": self.html,
            "tags": [t.name for t in self.tags]
        }
        return json.dumps(data)

    @staticmethod
    def from_json(data):
        post = json.loads(data)
        return Post(
            title=post.get("title"),
            timestamp=post.get("timestamp"),
            body=post.get("body"),
            html=post.get("html"),
            tags=[Tag.query.filter_by(name=t).first() for
                  t in post.get("tags")]
        )


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return "<Tag {name}>".format(name=self.name)

    def url(self):
        return url_for("tag", id=self.id)
