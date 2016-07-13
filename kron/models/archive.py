from flask import url_for
from flask import current_app as app
from hashids import Hashids

from kron.db import db


class Archive(db.Model):
    """"""

    __tableid__ = 101
    __tablename__ = 'archives'
    id = db.Column(db.Integer, primary_key=True)
    id_hash = db.Column(db.String(8), unique=True, index=True)
    name = db.Column(db.String(256))
    boxes = db.relationship('Box', backref='archive', lazy='dynamic')

    def __init__(self, name, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
        self.name = name

    def to_dict(self):
        rv = dict(
            uri=url_for(
                'ArchivesView:get', id=self.id_hash, _external=True),
            name=self.name,
            boxes=url_for(
                'ArchivesView:get_boxes', id=self.id_hash, _external=True)
        )
        for k in list(rv):
            if not rv[k]:
                del rv[k]
        return rv

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return '<Archive {id}-{h} "{n}">'.format(
        id=self.id, h=self.id_hash, n=self.name)


@db.event.listens_for(Archive, 'after_insert')
def after_insert(mapper, connection, target):
    """ Get a unique id hash for this Archive."""
    
    hid = Hashids(app.config['SECRET_KEY'], 8)
    base = Archive.__tableid__ + target.id
    id_hash = hid.encode(base)
    
    t = Archive.__table__
    if not target.id_hash:
        connection.execute(
            t.update().
                where(t.c.id==target.id).
                values(id_hash=id_hash)
        )

