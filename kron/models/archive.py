from datetime import datetime

from flask import url_for

from kron import db, uniqid


class Archive(db.Model):
    __tablename__ = "archives"
    __tableid__ = uniqid()
    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(8), unique=True, index=True)
    last_update = db.Column(db.DateTime)
    name = db.Column(db.String(128), unique=True, index=True)
    notes = db.Column(db.UnicodeText)
    boxes = db.relationship(
        "Box", lazy="dynamic",
        backref=db.backref("archive", lazy="joined"))
    
    def __init__(self, name):
        db.Model.__init__(self)
        self.id = Archive.__tableid__ + uniqid()
        self.last_update = datetime.now()
        self.name = name
    
    def to_dict(self):
        rv = dict(
            id=self.id,
            last_update=self.last_update,
            name=self.name
        )
        if self.notes:
            rv["notes"] = self.notes
        if self.boxes:
            rv["boxes"] = [dict(
                number=b.number,
                url=b.get_url()
            ) for b in self.boxes]
        return rv
    
    def get_url(self, full=False):
        return url_for("api.get_archive", name=self.name, _external=full)

    def __repr__(self):
        return "<Archive {name}>".format(name=self.name)
