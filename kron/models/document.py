import json

from kron import db


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
    authors = db.relationship("Person", secondary=documents_authors,
                              backref="documents_by")
    people = db.relationship("Person", secondary=documents_people,
                             backref="documents_in")
    topics = db.relationship("Topic", secondary=documents_topics,
                             backref="documents")
    box_id = db.Column(db.Integer, db.ForeignKey("boxes.id"))
    last_update = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "title": self.title,
            "authors": [a.name for a in self.authors],
            "people": [p.name for p in self.people],
            "topics": [t.name for t in self.topics],
            "box": self.box.number,
            "last_update": self.last_update,
            "notes": self.notes
        })

    def __repr__(self):
        return "<Document \"{title}\">".format(title=self.title)
