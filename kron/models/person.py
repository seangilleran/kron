from kron import db


people_topics = db.Table(
    "people_topics",
    db.Column("person_id", db.Integer, db.ForeignKey("people.id")),
    db.Column("topic_id", db.Integer, db.ForeignKey("topics.id"))
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
