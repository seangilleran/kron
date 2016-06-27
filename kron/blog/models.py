from kron import db


tags_posts = db.Table(
    "tags_posts",
    db.Column("post_tag_id", db.Integer, db.ForeignKey("post_tag.id")),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"))
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


class PostTag(db.Model):
    __tablename__ = "post_tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return "<Tag {name}>".format(name=self.name)
