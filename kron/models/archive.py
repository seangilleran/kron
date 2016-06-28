import json

from kron import db


class Archive(db.Model):
    __tablename__ = "archives"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    boxes = db.relationship("Box", backref="archive")
    last_update = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "boxes": [b.number for b in self.boxes],
            "last_update": self.last_update,
            "notes": self.notes
        })

    def __repr__(self):
        return "<Archive {name}>".format(name=self.name)
