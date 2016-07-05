from datetime import datetime

from flask import url_for

from kron import db, is_ok, ModelEventListeners


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
            raise TypeError("Missing data: person")
        if not is_ok(data.get("name")):
            raise TypeError("Missing data: person.name")
        if (Person.query.filter_by(name=data["name"]).first() or
           len(data["name"]) >= 128):
            raise TypeError("Invalid data: person.name")
        return Person(
            name=data["name"],
            dates=data.get("dates"),
            citations=data.get("citations"),
            notes=data.get("notes")
        )

    def get_url(self, full=False):
        return url_for("kron.get_person", id=self.id, _external=full)

    def __repr__(self):
        return "<Person {id}>".format(id=self.id)


db.event.listen(Person.name, "set", ModelEventListeners.on_update)
db.event.listen(Person.dates, "set", ModelEventListeners.on_update)
db.event.listen(Person.citations, "set", ModelEventListeners.on_update)
db.event.listen(Person.notes, "set", ModelEventListeners.on_update)
