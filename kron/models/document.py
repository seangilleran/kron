from datetime import datetime

from flask import url_for

from kron import db, is_ok, ModelEventListeners


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
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True)
    dates = db.Column(db.UnicodeText)
    citations = db.Column(db.UnicodeText)
    notes = db.Column(db.UnicodeText)
    last_update = db.Column(db.DateTime)
    box_id = db.Column(db.Integer, db.ForeignKey("boxes.id"))
    authors = db.relationship(
        "Person", secondary=documents_authors,
        backref=db.backref("documents_by", lazy="dynamic"))
    people = db.relationship(
        "Person", secondary=documents_people,
        backref=db.backref("documents_in", lazy="dynamic"))
    topics = db.relationship(
        "Topic", secondary=documents_topics, backref="documents")

    def __init__(self, title, dates=None, citations=None, notes=None):
        db.Model.__init__(self)
        self.title = title
        self.dates = dates
        self.citations = citations
        self.notes = notes

    @staticmethod
    def from_dict(data):
        data = data.get("document")
        if not is_ok(data):
            raise TypeError("Missing data: document")
        if not is_ok(data.get("title")):
            raise TypeError("Missing data: document.title")
        if (Document.query.filter_by(title=data["title"]).first() or
           len(data["title"]) >= 128):
            raise TypeError("Invalid data: document.title")
        return Document(
            title=data["title"],
            dates=data.get("dates"),
            citations=data.get("citations"),
            notes=data.get("notes")
        )

    def get_url(self, full=False):
        return url_for("kron.get_document", id=self.id, _external=full)

    def __repr__(self):
        return "<Document {id}>".format(id=self.id)


db.event.listen(Document.title, "set", ModelEventListeners.on_update)
db.event.listen(Document.box_id, "set", ModelEventListeners.on_update)
db.event.listen(Document.dates, "set", ModelEventListeners.on_update)
db.event.listen(Document.citations, "set", ModelEventListeners.on_update)
db.event.listen(Document.notes, "set", ModelEventListeners.on_update)
