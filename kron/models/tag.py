from flask import url_for

from kron.db import db
import kron.utils as u


class Tag(db.Model):

    __tableid__ = 401
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    id_hash = db.Column(db.String(8), unique=True, index=True)
    name = db.Column(db.String(256), unique=True)
    last_modified = db.Column(db.String(32))
    tagtype_id = db.Column(db.Integer, db.ForeignKey('tagtypes.id'))

    def __init__(self, name, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
        self.name = name

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'])

    def to_dict(self):
        rv = dict(
            name=self.name, uri=self.get_uri(),
            tagtype=dict(
                name=self.tagtype.name, uri=self.tagtype.get_uri()
            ) if self.tagtype else None
        )
        for key in list(rv):
            if not rv[key]:
                del rv[key]
        return rv

    def get_uri(self):
        return url_for('TagsView:get', id=self.id_hash, _external=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return '<Tag {id}-{h} "{n}">'.format(
            id=self.id, h=self.id_hash, n=self.name
        )


class TagType(db.Model):

    __tableid__ = 501
    __tablename__ = 'tagtypes'
    id = db.Column(db.Integer, primary_key=True)
    id_hash = db.Column(db.String(8), unique=True, index=True)
    name = db.Column(db.String(256), unique=True)
    last_modified = db.Column(db.String(32))
    tags = db.relationship('Tag', backref='tagtype', lazy='dynamic')

    def __init__(self, name, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
        self.name = name

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'])

    def to_dict(self):
        rv = dict(
            name=self.name, uri=self.get_uri(),
            tags=[dict(
                name=t.name, uri=t.get_uri()
            ) for t in self.tags] if self.tags.first() else None
        )
        for key in list(rv):
            if not rv[key]:
                del rv[key]
        return rv

    def get_uri(self):
        return url_for('TagsView:get_tagtype', id=self.id_hash, _external=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return '<TagType {id}-{h} "{n}">'.format(
            id=self.id, h=self.id_hash, n=self.name
        )


@db.event.listens_for(Tag, 'after_insert')
def after_insert(mapper, connection, target):
    u.update_event(Tag, connection, target)


@db.event.listens_for(Tag, 'after_update')
def after_update(mapper, connection, target):
    u.update_event(Tag, connection, target)


@db.event.listens_for(TagType, 'after_insert')
def after_insert(mapper, connection, target):
    u.update_event(TagType, connection, target)


@db.event.listens_for(TagType, 'after_update')
def after_update(mapper, connection, target):
    u.update_event(TagType, connection, target)

