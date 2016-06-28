from kron import db


class Citation(db.Model):
    __tablename__ = "citations"
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(256))
    text = db.Column(db.Text)
    notes = db.relationship("Note", backref="citation")

    def __repr__(self):
        return "<Citation {loc}>".format(loc=self.location)
