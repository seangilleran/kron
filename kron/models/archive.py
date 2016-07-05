from datetime import datetime

from flask import url_for
from flask_wtf import Form
from wtforms import StringField, TextField
from wtforms.validators import DataRequired, Optional, Length

from kron import db, is_ok, ModelEventListeners


class Archive(db.Model):
    __tablename__ = "archives"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    notes = db.Column(db.UnicodeText)
    last_update = db.Column(db.DateTime)
    boxes = db.relationship("Box", backref="archive")

    def __init__(self, name, notes=""):
        db.Model.__init__(self)
        self.name = name
        self.notes = notes

    @staticmethod
    def from_dict(data, archive=None):
        data = data.get("archive")
        if not is_ok(data):
            raise TypeError("Missing data: archive")
        
        if not is_ok(data.get("name")):
            raise TypeError("Missing data: archive.name")
        if (Archive.query.filter_by(name=data["name"]).first() or
           len(data["name"]) >= 128):
            raise TypeError("Invalid data: archive.name")
        return Archive(
            name=data["name"], notes=data.get("notes", "")
        )

    def from_form(self, form):
        self.name = form.get("name", self.name)
        self.notes = form.get("notes", self.notes)

    def get_form(self, form=None):
        rv = ArchiveForm() if not form else form
        rv.name.data = self.name
        rv.notes = self.notes
        return rv

    def get_url(self, param=None, full=False):
        return url_for(
            "kron.get_archive", id=self.id, param=param, _external=full)

    def __repr__(self):
        return "<Archive {id}>".format(id=self.id)


db.event.listen(Archive.name, "set", ModelEventListeners.on_update)
db.event.listen(Archive.notes, "set", ModelEventListeners.on_update)


class ArchiveForm(Form):
    name = StringField("Name", [DataRequired(), Length(1, 128)])
    notes = TextField("Notes", [Optional()])
