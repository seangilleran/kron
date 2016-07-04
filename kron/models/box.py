from datetime import datetime

from flask import url_for

from kron import db, is_ok, ModelEventListeners
from kron.exceptions import APIInvalidUsage


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
            raise APIInvalidUsage("Missing data: box")
        if not is_ok(data.get("number")):
            raise APIInvalidUsage("Missing data: box.number")
        return Box(
            number=data["number"],
            dates=data.get("dates"),
            notes=data.get("notes")
        )

    def update_from_dict(self, data):
        data = data.get("box")
        if not is_ok(data):
            raise APIInvalidUsage("Missing data: box")
        self.number = data.get("number", self.number)
        if is_ok(data.get("dates")):
            self.dates = data["dates"]
        if is_ok(data.get("notes")):
            self.notes = data["notes"]

    def to_dict(self):
        rv = dict(box=dict(
            id=self.id, number=self.number,
            dates=self.dates,
            notes=self.notes,
            last_update=datetime.strftime(
                self.last_update, '%b %d %Y %I:%M%p'),
            documents=[dict(url=d.get_url()) for d in self.documents],
            people=[dict(url=d.get_url()) for p in self.people],
            topics=[dict(url=t.get_url()) for t in self.topics],
            url=self.get_url()
        ))
        for key in list(rv["box"]):
            if not is_ok(rv["box"][key]):
                rv["box"].pop(key, None)
        return rv

    def get_url(self, full=False):
        return url_for("api.get_box", id=self.id, _external=full)

    def __repr__(self):
        return "<Box {id}>".format(id=self.id)


db.event.listen(Box.number, "set", ModelEventListeners.on_update)
db.event.listen(Box.dates, "set", ModelEventListeners.on_update)
db.event.listen(Box.notes, "set", ModelEventListeners.on_update)
db.event.listen(Box.archive_id, "set", ModelEventListeners.on_update)
