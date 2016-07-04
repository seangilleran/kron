from datetime import datetime

from flask import url_for

from kron import db, is_ok, ModelEventListeners
from kron.exceptions import APIInvalidUsage


class Archive(db.Model):
    __tablename__ = "archives"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    notes = db.Column(db.UnicodeText)
    last_update = db.Column(db.DateTime)
    boxes = db.relationship("Box", backref="archive")

    def __init__(self, name, notes=None):
        db.Model.__init__(self)
        self.name = name
        self.notes = notes

    @staticmethod
    def from_dict(data):
        if not is_ok(data.get("archive")):
            raise APIInvalidUsage("Missing data: archive")
        if not is_ok(data["archive"].get("name")):
            raise APIInvalidUsage("Missing data: archive.name")
        return Archive(
            name=data["archive"]["name"],
            notes=data["archive"].get("notes")
        )

    def update_from_dict(self, data):
        archive = data.get("archive")
        if not archive:
            raise APIInvalidUsage("Missing data: archive")
        self.name = archive.get("name", self.name)
        self.notes = archive.get("notes", self.notes)

    def to_dict(self):
        rv = dict(archive=dict(
            id=self.id, name=self.name,
            notes=self.notes,
            last_update=datetime.strftime(
                self.last_update, '%b %d %Y %I:%M%p'),
            boxes=[dict(url=b.get_url()) for b in self.boxes],
            url=self.get_url()
        ))
        for key in list(rv["archive"]):
            if not is_ok(rv["archive"][key]):
                rv["archive"].pop(key, None)
        return rv

    def get_url(self, full=False):
        return url_for("api.get_archive", id=self.id, _external=full)

    def __repr__(self):
        return "<Archive {id}>".format(id=self.id)


db.event.listen(Archive.name, "set", ModelEventListeners.on_update)
db.event.listen(Archive.notes, "set", ModelEventListeners.on_update)
