from kron.db import db
import kron.utils as u


class Box(db.Model):

    __tableid__ = 201
    __tablename__ = 'boxes'
    id = db.Column(db.Integer, primary_key=True)
    id_hash = db.Column(db.String(8), unique=True, index=True)
    name = db.Column(db.String(256))
    last_modified = db.Column(db.String(32))
    archive_id = db.Column(db.Integer, db.ForeignKey('archives.id'))
    documents = db.relationship('Document', backref='box', lazy='dynamic')

    def __init__(self, name, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
        self.name = name

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'])

    def to_dict(self):
        rv = dict(
            name=self.name, uri=self.get_uri(),
            archive=dict(
                name=self.archive.name, uri=self.archive.get_uri()
            ) if self.archive else None,
            documents=[dict(
                name=d.name, uri=d.get_uri()
            ) for d in self.documents] if self.documents.first() else None
        )
        for key in list(rv):
            if not rv[key]:
                del rv[key]
        return rv

    def get_uri(self):
        from flask import url_for

        return url_for('BoxesView:get', id=self.id_hash, _external=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return '<Box {id}-{h} "{n}">'.format(
            id=self.id, h=self.id_hash, n=self.name
        )


@db.event.listens_for(Box, 'after_insert')
def after_insert(mapper, connection, target):
    u.update_event(Box, connection, target)


@db.event.listens_for(Box, 'after_update')
def after_update(mapper, connection, target):
    u.update_event(Box, connection, target)
