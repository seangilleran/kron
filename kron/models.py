from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Archive(db.Model):
    __tablename__ = "archieves"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    boxes = db.relationship("Box", backref="archive")
    notes = db.relationship("Note", backref="archive")

    def __repr__(self):
        return "<Archive {name}".format(name=self.name)


boxes_people = db.Table(
    "boxes_people",
    db.Column("box_id", db.Integer, db.ForeignKey("box.id")),
    db.Column("person_id", db.Integer, db.ForeignKey("person.id"))
)

boxes_topics = db.Table(
    "boxes_topics",
    db.Column("box_id", db.Integer, db.ForeignKey("box.id")),
    db.Column("topic_id", db.Integer, db.ForeignKey("topic.id"))
)


class Box(db.Model):
    __tablename__ = "boxes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    number = db.Column(db.Integer)
    archive_id = db.Column(db.Integer, db.ForeignKey("archive.id"))
    people = db.relationship("Person", secondary=boxes_people, backref="boxes")
    topics = db.relationship("Topic", secondary=boxes_topics, backref="boxes")
    documents = db.relationship("Document", backref="box")
    notes = db.relationship("Note", backref="box")

    def __repr__(self):
        return "<Box #{num}".format(num=self.number)


documents_authors = db.Table(
    "documents_authors",
    db.Column("document_id", db.Integer, db.ForeignKey("document.id")),
    db.Column("person_id", db.Integer, db.ForeignKey("person.id"))
)

documents_people = db.Table(
    "documents_people",
    db.Column("document_id", db.Integer, db.ForeignKey("document.id")),
    db.Column("person_id", db.Integer, db.ForeignKey("person.id"))
)

documents_topics = db.Table(
    "documents_topics",
    db.Column("document_id", db.Integer, db.ForeignKey("document.id")),
    db.Column("topic_id", db.Integer, db.ForeignKey("topic.id"))
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
    box_id = db.Column(db.Integer, db.ForeignKey("box.id"))
    notes = db.relationship("Note", backref="document")

    def __repr__(self):
        return "<Document \"{title}\">".format(title=self.title)


people_topics = db.Table(
    "people_topics",
    db.Column("person_id", db.Integer, db.ForeignKey("person.id")),
    db.Column("topic_id", db.Integer, db.ForeignKey("topic.id"))
)


class Person(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    topics = db.relationship("Topic", secondary=people_topics,
                             backref="people")
    notes = db.relationship("Note", backref="person")

    def __repr__(self):
        return "<Person {name}>".format(name=self.name)


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    html = db.Column(db.Text)

    def __repr__(self):
        return "<Note #{num}>".format(num=self.id)


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    notes = db.relationship("Note", backref="topic")

    def __repr__(self):
        return "<Topic {name}>".format(name=self.name)
