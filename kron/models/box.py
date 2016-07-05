from datetime import datetime

from flask import url_for

from kron import db, is_ok, ModelEventListeners


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
    dates = db.Column(db.UnicodeText)
    notes = db.Column(db.UnicodeText)
    last_update = db.Column(db.DateTime)
    archive_id = db.Column(db.Integer, db.ForeignKey("archives.id"))
    documents = db.relationship("Document", backref="box")
    people = db.relationship(
        "Person", secondary=boxes_people, backref="boxes")
    topics = db.relationship(
        "Topic", secondary=boxes_topics, backref="boxes")

    def __init__(self, number, dates=None, notes=None):
        db.Model.__init__(self)
        self.number = number
        self.dates = dates
        self.notes = notes

    @staticmethod
    def from_dict(data):
        data = data.get("box")
        if not is_ok(data):
            raise TypeError("Missing data: box")
        if not is_ok(data.get("number")):
            raise TypeError("Missing data: box.number")
        if Box.query.filter_by(number=data["number"]).first():
            raise TypeError("Invalid data: box.number")
        return Box(
            number=data["number"],
            dates=data.get("dates"),
            notes=data.get("notes")
        )

    def get_url(self, full=False):
        return url_for("kron.get_box", id=self.id, _external=full)

    def __repr__(self):
        return "<Box {id}>".format(id=self.id)


db.event.listen(Box.number, "set", ModelEventListeners.on_update)
db.event.listen(Box.dates, "set", ModelEventListeners.on_update)
db.event.listen(Box.notes, "set", ModelEventListeners.on_update)
db.event.listen(Box.archive_id, "set", ModelEventListeners.on_update)
