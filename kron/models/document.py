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
    title = db.Column(db.String(128))
    authors = db.relationship("Person", secondary=documents_authors,
                              backref="documents_by")
    people = db.relationship("Person", secondary=documents_people,
                             backref="documents_in")
    topics = db.relationship("Topic", secondary=documents_topics,
                             backref="documents")
    box_id = db.Column(db.Integer, db.ForeignKey("boxes.id"))
    notes = db.relationship("Note", backref="document")

    def __repr__(self):
        return "<Document \"{title}\">".format(title=self.title)
