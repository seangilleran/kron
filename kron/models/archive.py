from flask import url_for

from kron.db import db
import kron.utils as u


class Archive(db.Model):

    __tableid__ = 101
    __tablename__ = 'archives'
    id = db.Column(db.Integer, primary_key=True)
    id_hash = db.Column(db.String(8), unique=True, index=True)
    name = db.Column(db.String(256), unique=True)
    last_modified = db.Column(db.String(32))
    boxes = db.relationship('Box', backref='archive', lazy='dynamic')

    def __init__(self, name, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
        self.name = name

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        rv = dict(
            name=self.name, uri=self.get_uri(),
            boxes=[dict(
                name=b.name, uri=b.get_uri()
            ) for b in self.boxes] if self.boxes.first() else None
        )
        for key in list(rv):
            if not rv[key]:
                del rv[key]
        return rv

    def get_uri(self):
        return url_for('ArchivesView:get', id=self.id_hash, _external=True)

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return '<Archive {id}-{h} "{n}">'.format(
            id=self.id, h=self.id_hash, n=self.name
        )


@db.event.listens_for(Archive, 'after_insert')
def after_insert(mapper, connection, target):
    u.update_event(Archive, connection, target)


@db.event.listens_for(Archive, 'after_update')
def after_update(mapper, connection, target):
    u.update_event(Archive, connection, target)
