from kron import db


class Archive(db.Model):
    __tablename__ = "archives"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    boxes = db.relationship("Box", backref="archive")
    notes = db.relationship("Note", backref="archive")

    def __repr__(self):
        return "<Archive {name}".format(name=self.name)
