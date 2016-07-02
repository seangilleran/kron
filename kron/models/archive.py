from datetime import datetime
from re import sub

from flask import url_for, current_app
from markdown import markdown
import bleach

from kron import db, uniqid


class Archive(db.Model):
    __tablename__ = "archives"
    __tableid__ = uniqid()
    _id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.String(8), unique=True, index=True)
    last_update = db.Column(db.DateTime)
    name = db.Column(db.String(128), unique=True, index=True)
    full_name = db.Column(db.String(128))
    notes = db.Column(db.UnicodeText)
    notes_html = db.Column(db.UnicodeText)
    boxes = db.relationship(
        "Box", lazy="dynamic",
        backref=db.backref("archive", lazy="joined"))

    def __init__(self, name):
        db.Model.__init__(self)
        self.id = Archive.__tableid__ + uniqid()
        self.full_name = name

    @staticmethod
    def on_update(target, value, oldvalue, initiator):
        target.last_update = datetime.now()

    @staticmethod
    def on_update_name(target, value, oldvalue, initiator):
        target.name = sub("[^A-Za-z]", "_", value).lower()

    @staticmethod
    def on_update_notes(target, value, oldvalue, initiator):
        allowed_tags = current_app.config.get("ALLOWED_HTML_TAGS")
        html = markdown(value, output_format="html")
        target.notes_html = bleach.linkify(
            bleach.clean(html, tags=allowed_tags, strip=True))

    def to_dict(self):
        rv = dict(Archive=dict(
            id=self.id,
            last_update=self.last_update,
            name=self.full_name,
            url=self.get_url()
        ))
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
        return "<Archive {id}>".format(id=self.id)


db.event.listen(Archive.full_name, "set", Archive.on_update)
db.event.listen(Archive.full_name, "set", Archive.on_update_name)
db.event.listen(Archive.notes, "set", Archive.on_update)
db.event.listen(Archive.notes, "set", Archive.on_update_notes)
db.event.listen(Archive.boxes, "set", Archive.on_update)
