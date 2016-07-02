import json

from kron import db


class Archive(db.Model):
    __tablename__ = "archives"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    boxes = db.relationship(
        "Box", lazy="dynamic",
        backref=db.backref("archive", lazy="joined"))
    last_update = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    def __repr__(self):
        return "<Archive {name}>".format(name=self.name)
