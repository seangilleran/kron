import json

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
    number = db.Column(db.Integer, unique=True)
    archive_id = db.Column(db.Integer, db.ForeignKey("archives.id"))
    people = db.relationship("Person", secondary=boxes_people, backref="boxes")
    topics = db.relationship("Topic", secondary=boxes_topics, backref="boxes")
    documents = db.relationship("Document", backref="box")
    last_update = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "number": self.number,
            "archive": self.archive.name,
            "people": [p.name for p in people],
            "topics": [t.name for t in topics],
            "documents": [d.title for d in documents],
            "last_update": self.last_update,
            "notes": self.notes
        })

    def __repr__(self):
        return "<Box #{num}>".format(num=self.number)
