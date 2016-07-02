from datetime import datetime

from flask import url_for

from kron import db, uniqid


people_topics = db.Table(
    "people_topics",
    db.Column("person_id", db.Integer, db.ForeignKey("people.id")),
    db.Column("topic_id", db.Integer, db.ForeignKey("topics.id"))
)


class Person(db.Model):
    __tablename__ = "people"
    __tableid__ = uniqid()
    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(8), unique=True, index=True)
    last_update = db.Column(db.DateTime)
    name = db.Column(db.String(128), unique=True, index=True)
    citations = db.Column(db.UnicodeText)
    notes = db.Column(db.UnicodeText)
    topics = db.relationship(
        "Topic", secondary=people_topics, lazy="joined",
        backref=db.backref("people", lazy="joined"))

    def __init__(self, name):
        db.Model.__init__(self)
        self.id = Person.__tableid__ + uniqid()
        self.last_update = datetime.now()
        self.name = name
    
    def to_dict(self):
        rv = dict(
            id=self.id,
            last_update=self.last_update,
            name=self.name
        )
        if self.citations:
            rv["citations"] = self.citations
        if self.notes:
            rv["notes"] = self.notes
        if self.topics:
            rv["topics"] = [dict(
                name=t.name,
                url=t.get_url()
            ) for t in self.topics]
        if self.boxes:
            rv["boxes"] = [dict(
                number=b.number,
                url=b.get_url()
            ) for b in self.boxes]
        if self.documents_by:
            rv["documents_by"] = [dict(
                id=d.id,
                title=d.title,
                url=d.get_url()
            ) for d in self.documents_by]
        if self.documents_in:
            rv["documents_in"] = [dict(
                id=d.id,
                title=d.title,
                url=d.get_url()
            ) for d in self.documents_in]
        return rv
    
    def get_url(self, full=False):
        return url_for("api.get_person", name=self.name, _external=full)

    def __repr__(self):
        return "<Person {name}>".format(name=self.name)
