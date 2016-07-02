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
    number = db.Column(db.Integer, unique=True, index=True)
    archive_id = db.Column(db.Integer, db.ForeignKey("archives.id"))
    people = db.relationship(
        "Person", secondary=boxes_people, lazy="joined",
        backref=db.backref("boxes", lazy="dynamic"))
    topics = db.relationship(
        "Topic", secondary=boxes_topics, lazy="joined",
        backref=db.backref("boxes", lazy="dynamic"))
    documents = db.relationship(
        "Document", lazy="joined", backref=db.backref("box", lazy="joined"))
    last_update = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    def __repr__(self):
        return "<Box #{num}>".format(num=self.number)
