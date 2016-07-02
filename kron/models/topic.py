from datetime import datetime

from flask import url_for

from kron import db, uniqid


class Topic(db.Model):
    __tablename__ = "topics"
    __tableid__ = uniqid()
    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(8), unique=True, index=True)
    name = db.Column(db.String(128), unique=True, index=True)
    last_update = db.Column(db.DateTime)
    citations = db.Column(db.Text)
    notes = db.Column(db.Text)

    def __init__(self, name):
        db.Model.__init__(self)
        self.id = Topic.__tableid__ + uniqid()
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
        if self.boxes:
            rv["boxes"] = [dict(
                number=b.number,
                url=b.get_url()
            ) for b in self.boxes]
        if self.documents:
            rv["documents"] = [dict(
                id=d.id,
                title=d.title,
                url=d.get_url()
            ) for d in self.documents]
        if self.people:
            rv["people"] = [dict(
                name=p.name,
                url=p.get_url()
            ) for p in self.people]
        return rv

    def get_url(self, full=False):
        return url_for("api.get_topic", name=self.name, _external=full)

    def __repr__(self):
        return "<Topic {name}>".format(name=self.name)
