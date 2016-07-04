from datetime import datetime

from flask import url_for

from kron import db, is_ok, ModelEventListeners
from kron.exceptions import APIInvalidUsage


people_topics = db.Table(
    "people_topics",
    db.Column("person_id", db.Integer, db.ForeignKey("people.id")),
    db.Column("topic_id", db.Integer, db.ForeignKey("topics.id"))
)


class Person(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    dates = db.Column(db.UnicodeText)
    citations = db.Column(db.UnicodeText)
    notes = db.Column(db.UnicodeText)
    last_update = db.Column(db.DateTime)
    topics = db.relationship(
        "Topic", secondary=people_topics, backref="people")

    def __init__(self, name, dates=None, citations=None, notes=None):
        db.Model.__init__(self)
        self.name = name
        self.dates = dates
        self.citations = citations
        self.notes = notes

    @staticmethod
    def from_dict(data):
        data = data.get("person")
        if not is_ok(data):
            raise APIInvalidUsage("Missing data: person")
        if not is_ok(data.get("name")):
            raise APIInvalidUsage("Missing data: person.name")
        return Person(
            name=data["name"],
            dates=data.get("dates"),
            citations=data.get("citations"),
            notes=data.get("notes")
        )

    def update_from_dict(self, data):
        data = data.get("person")
        if not is_ok(data):
            raise APIInvalidUsage("Missing data: person")
        if is_ok(data.get("name")):
            self.name = data["name"]
        if is_ok(data.get("dates")):
            self.dates = data["dates"]
        if is_ok(data.get("citations")):
            self.citations = data["citations"]
        if is_ok(data.get("notes")):
            self.notes = data["notes"]

    def to_dict(self):
        rv = dict(person=dict(
            id=self.id, name=self.name,
            dates=self.dates,
            citations=self.citations,
            notes=self.notes,
            last_update=datetime.strftime(
                self.last_update, '%b %d %Y %I:%M%p'),
            topics=[dict(url=t.get_url()) for t in self.topics],
            boxes=[dict(url=b.get_url()) for b in self.boxes],
            documents_by=[dict(url=d.get_url()) for d in self.documents_by],
            documents_in=[dict(url=d.get_url()) for d in self.documents_in],
            url=self.get_url()
        ))
        for key in list(rv["person"]):
            if not is_ok(rv["person"][key]):
                rv["person"].pop(key, None)
        return rv

    def get_url(self, full=False):
        return url_for("api.get_person", id=self.id, _external=full)

    def __repr__(self):
        return "<Person {id}>".format(id=self.id)


db.event.listen(Person.name, "set", ModelEventListeners.on_update)
db.event.listen(Person.dates, "set", ModelEventListeners.on_update)
db.event.listen(Person.citations, "set", ModelEventListeners.on_update)
db.event.listen(Person.notes, "set", ModelEventListeners.on_update)
