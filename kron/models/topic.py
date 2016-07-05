from datetime import datetime

from flask import url_for

from kron import db, is_ok, ModelEventListeners


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    dates = db.Column(db.UnicodeText)
    citations = db.Column(db.UnicodeText)
    notes = db.Column(db.UnicodeText)
    last_update = db.Column(db.DateTime)

    def __init__(self, name, dates=None, citations=None, notes=None):
        db.Model.__init__(self)
        self.name = name
        self.dates = dates
        self.citations = citations
        self.notes = notes

    @staticmethod
    def from_dict(data):
        data = data.get("topic")
        if not is_ok(data):
            raise TypeError("Missing data: topic")
        if not is_ok(data.get("name")):
            raise TypeError("Missing data: topic.name")
        return Topic(
            name=data["name"],
            dates=data.get("dates"),
            citations=data.get("citations"),
            notes=data.get("notes")
        )

    def get_url(self, full=False):
        return url_for("kron.get_topic", id=self.id, _external=full)

    def __repr__(self):
        return "<Topic {id}>".format(id=self.id)


db.event.listen(Topic.name, "set", ModelEventListeners.on_update)
db.event.listen(Topic.dates, "set", ModelEventListeners.on_update)
db.event.listen(Topic.citations, "set", ModelEventListeners.on_update)
db.event.listen(Topic.notes, "set", ModelEventListeners.on_update)
