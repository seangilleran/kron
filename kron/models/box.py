from kron import db


boxes_people = db.Table(
    "boxes_people",
    db.Column("box_id", db.Integer, db.ForeignKey("boxes.id")),
    db.Column("person_id", db.Integer, db.ForeignKey("people.id"))
)

boxes_topics = db.Table(
    "boxes_topics",
    db.Column("box_id", db.Integer, db.ForeignKey("boxes.id")),
    db.Column("topic_id", db.Integer, db.ForeignKey("topics.id"))
)


class Box(db.Model):
    __tablename__ = "boxes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    number = db.Column(db.Integer)
    archive_id = db.Column(db.Integer, db.ForeignKey("archives.id"))
    people = db.relationship("Person", secondary=boxes_people, backref="boxes")
    topics = db.relationship("Topic", secondary=boxes_topics, backref="boxes")
    documents = db.relationship("Document", backref="box")
    notes = db.relationship("Note", backref="box")

    def __repr__(self):
        return "<Box #{num}".format(num=self.number)
