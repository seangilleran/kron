from flask import url_for

from kron.db import db
import kron.utils as u


documents_tags = db.Table(
    'documents_tags',
    db.Column('document_id', db.Integer, db.ForeignKey('documents.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')))


class Document(db.Model):

    __tableid__ = 301
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    id_hash = db.Column(db.String(8), unique=True, index=True)
    name = db.Column(db.String(256), unique=True)
    img_url = db.Column(db.String(256))
    last_modified = db.Column(db.String(32))
    box_id = db.Column(db.Integer, db.ForeignKey('boxes.id'))
    tags = db.relationship(
        'Tag', secondary=documents_tags, backref='documents')

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
            img_url=self.img_url,
            box=dict(
                name=self.box.name, uri=self.box.get_uri()
            ) if self.box else None
        )
        for key in list(rv):
            if not rv[key]:
                del rv[key]
        return rv

    def get_uri(self):
        return url_for('DocumentsView:get', id=self.id_hash, _external=True)

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return '<Document {id}-{h} "{n}">'.format(
            id=self.id, h=self.id_hash, n=self.name
        )


@db.event.listens_for(Document, 'after_insert')
def after_insert(mapper, connection, target):
    u.update_event(Document, connection, target)


@db.event.listens_for(Document, 'after_update')
def after_update(mapper, connection, target):
    u.update_event(Document, connection, target)

