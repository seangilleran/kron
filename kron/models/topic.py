from kron import db


topics_citations = db.Table(
    "topics_citations",
    db.Column("topic_id", db.Integer, db.ForeignKey("topics.id")),
    db.Column("citation_id", db.Integer, db.ForeignKey("citations.id"))
)


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    citations = db.relationship("Citation", secondary=topics_citations,
                                backref="topics")
    notes = db.relationship("Note", backref="topic")

    def __repr__(self):
        return "<Topic {name}>".format(name=self.name)
