from kron import db


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    notes = db.relationship("Note", backref="topic")

    def __repr__(self):
        return "<Topic {name}>".format(name=self.name)
