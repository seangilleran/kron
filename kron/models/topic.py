from datetime import datetime

from flask import url_for

from kron import db, is_ok, ModelEventListeners
from kron.exceptions import APIInvalidUsage


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
            raise APIInvalidUsage("Missing data: topic")
        if not is_ok(data.get("name")):
            raise APIInvalidUsage("Missing data: topic.name")
        return Topic(
            name=data["name"],
            dates=data.get("dates"),
            citations=data.get("citations"),
            notes=data.get("notes")
        )

    def update_from_dict(data):
        data = data.get("topic")
        if not is_ok(data):
            raise APIInvalidUsage("Missing data: topic")
        if is_ok(data.get("name")):
            self.name = data["name"]
        if is_ok(data.get("dates")):
            self.dates = data["dates"]
        if is_ok(data.get("citations")):
            self.citations = data["citations"]
        if is_ok(data.get("notes")):
            self.notes = data["notes"]

    def to_dict(self):
        rv = dict(topic=dict(
            id=self.id, name=self.name,
            dates=self.dates,
            citations=self.citations,
            notes=self.notes,
            last_update=datetime.strftime(
                self.last_update, '%b %d %Y %I:%M%p'),
            boxes=[dict(url=b.get_url()) for b in self.boxes],
            documents=[dict(url=d.get_url()) for d in self.documents],
            people=[dict(url=p.get_url()) for p in self.people],
            url=self.get_url()
        ))
        for key in list(rv["topic"]):
            if not is_ok(rv["topic"][key]):
                rv["topic"].pop(key, None)
        return rv

    def get_url(self, full=False):
        return url_for("api.get_topic", id=self.id, _external=full)

    def __repr__(self):
        return "<Topic {id}>".format(id=self.id)


db.event.listen(Topic.name, "set", ModelEventListeners.on_update)
db.event.listen(Topic.dates, "set", ModelEventListeners.on_update)
db.event.listen(Topic.citations, "set", ModelEventListeners.on_update)
db.event.listen(Topic.notes, "set", ModelEventListeners.on_update)
