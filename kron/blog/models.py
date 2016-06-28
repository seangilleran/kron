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
    def from_json(data):
        try:
            json_data = json.loads(data)
        except:
            return None
        return Post(
            title=json_data.get("title"),
            timestamp=datetime.strptime(
                json_data.get("timestamp"), "%m %d %Y"),
            body=json_data.get("body"),
            tags=[Tag.query.filter_by(t=id).first() for
                  t in json_data.get("tag_ids")]
        )

    def get_url(self, full=False):
        return url_for("blog.get_post", id=self.id, _external=full)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "timestamp": self.timestamp.strftime("%m %d %Y"),
            "body": self.body,
            "html": self.html,
            "tags": [t.get_url() for t in self.tags],
            "tag_ids": [t.id for t in self.tags],
            "url": self.get_url()
        }

    def __repr__(self):
        return "<Post {id}>".format(id=self.id)


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def get_url(self, full=False):
        return url_for("blog.get_tag", id=self.id, _external=full)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "posts": [p.get_url() for p in self.posts],
            "post_ids": [p.id for p in self.posts]
        }

    def __repr__(self):
        return "<Tag {name}>".format(name=self.name)
