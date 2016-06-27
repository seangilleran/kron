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
        backref=db.backref("tags_posts", lazy="joined")
    )

    def __repr__(self):
        return "<Post {id}>".format(id=self.id)


class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return "<Tag {name}>".format(name=self.name)
