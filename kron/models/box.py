from datetime import datetime

from flask import url_for

from kron import db, uniqid


boxes_people = db.Table(
    "boxes_people",
    db.Column("box_id", db.Integer, db.ForeignKey("boxes.id")),
    db.Column("person_id", db.Integer, db.ForeignKey("people.id"))
)

boxes_topics = db.Table(
    "boxes_topics",
    db.Column("box_id", db.Integer, db.ForeignKey("boxes.id")),
    db.Column("topic_id", db.Integer, db.ForeignKey("topics.id"))
)


class Box(db.Model):
    __tablename__ = "boxes"
    __tableid__ = uniqid()
    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(8), unique=True, index=True)
    last_update = db.Column(db.DateTime)
    number = db.Column(db.Integer, unique=True, index=True)
    archive_id = db.Column(db.Integer, db.ForeignKey("archives.id"))
    notes = db.Column(db.UnicodeText)
    people = db.relationship(
        "Person", secondary=boxes_people, lazy="joined",
        backref=db.backref("boxes", lazy="joined"))
    topics = db.relationship(
        "Topic", secondary=boxes_topics, lazy="joined",
        backref=db.backref("boxes", lazy="joined"))
    documents = db.relationship(
        "Document", lazy="joined", backref=db.backref("box", lazy="joined"))

    def __init__(self, number, archive):
        db.Model.__init__(self)
        self.id = Box.__tableid__ + uniqid()
        self.last_update = datetime.now()
        self.number = number
        self.archive_id = archive.id
    
    def to_dict(self):
        rv = dict(
            id = self.id,
            number = self.number,
            archive = dict(
                name=self.archive.name,
                url=self.archive.get_url()
            )
        )
        if self.notes:
            rv["notes"] = self.notes
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
        if self.documents:
            rv["documents"] = [dict(
                title=d.title,
                url=d.get_url()
            ) for d in self.documents]
        return rv
        
    def get_url(self, full=False):
        return url_for("api.get_box", number=self.number, _external=full)

    def __repr__(self):
        return "<Box #{num}>".format(num=self.number)
