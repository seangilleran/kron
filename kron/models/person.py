import json

from kron import db


people_topics = db.Table(
    "people_topics",
    db.Column("person_id", db.Integer, db.ForeignKey("people.id")),
    db.Column("topic_id", db.Integer, db.ForeignKey("topics.id"))
)


class Person(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    topics = db.relationship("Topic", secondary=people_topics,
                             backref="people")
    citations = db.Column(db.Text)
    last_update = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "name": self.id,
            "topics": [t.name for t in self.topics],
            "citations": self.citations,
            "last_update": self.last_update,
            "notes": self.notes
        })

    def __repr__(self):
        return "<Person {name}>".format(name=self.name)
