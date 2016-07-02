import json

from kron import db


class Topic(db.Model):
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    citations = db.Column(db.Text)
    last_update = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    def __repr__(self):
        return "<Topic {name}>".format(name=self.name)
