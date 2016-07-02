from datetime import datetime

from flask import url_for

from kron import db, uniqid


documents_authors = db.Table(
    "documents_authors",
    db.Column("document_id", db.Integer, db.ForeignKey("documents.id")),
    db.Column("person_id", db.Integer, db.ForeignKey("people.id"))
)

documents_people = db.Table(
    "documents_people",
    db.Column("document_id", db.Integer, db.ForeignKey("documents.id")),
    db.Column("person_id", db.Integer, db.ForeignKey("people.id"))
)

documents_topics = db.Table(
    "documents_topics",
    db.Column("document_id", db.Integer, db.ForeignKey("documents.id")),
    db.Column("topic_id", db.Integer, db.ForeignKey("topics.id"))
)


class Document(db.Model):
    __tablename__ = "documents"
    __tableid__ = uniqid()
    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(8), unique=True, index=True)
    last_update = db.Column(db.DateTime)
    title = db.Column(db.String(128), unique=True)
    notes = db.Column(db.Text)
    authors = db.relationship(
        "Person", secondary=documents_authors, lazy="joined",
        backref=db.backref("documents_by", lazy="joined"))
    people = db.relationship(
        "Person", secondary=documents_people, lazy="joined",
        backref=db.backref("documents_in", lazy="joined"))
    topics = db.relationship(
        "Topic", secondary=documents_topics, lazy="joined",
        backref=db.backref("documents", lazy="joined"))
    box_id = db.Column(db.Integer, db.ForeignKey("boxes.id"))

    def __init__(self, title):
        db.Model.__init__(self)
        self.id = Document.__tableid__ + uniqid()
        self.last_update = datetime.now()
        self.title = title
    
    def to_dict(self):
        rv = dict(
            id=self.id,
            last_update=self.last_update,
            title=self.title
        )
        if self.notes:
            rv["notes"] = self.notes
        if self.authors:
            rv["authors"] = [dict(
                name=a.name,
                url=a.get_url()
            ) for a in self.authors]
        if self.people:
            rv["people"] = [dict(
                name=p.name,
                url=p.get_url()
            ) for p in self.people]
        if self.topics:
            rv["topics"] = [dict(
                name=t.name,
                url=t.get_url()
            ) for t in self.topics]
        if self.box:
            rv["box"] = dict(
                number=self.box.number,
                url=self.box.get_url()
            )
        return rv
    
    def get_url(self, full=False):
        return url_for("api.get_document", id=self.id, _external=full)

    def __repr__(self):
        return "<Document \"{title}\">".format(title=self.title)
