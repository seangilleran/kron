from datetime import datetime
import json

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment


db = SQLAlchemy()
moment = Moment()


def is_ok(data):
    if not data or data == "" or data == [] or data == {} or data == [{}]:
        return False
    return True


def restore_from_file(path, drop=True):
    from kron import Tag, Post, Archive, Box, Document, Person, Topic

    if drop:
        db.drop_all()
        db.create_all()

    with open(path) as data_file:
        data = json.load(data_file)

    print("Loading tags...")
    for i in data["tags"]:
        t = Tag.from_dict(i)
        db.session.add(t)
    db.session.commit()

    print("Loading posts...")
    for i in data["posts"]:
        p = Post.from_dict(i)
        p.tags.extend([Tag.query.filter_by(id=t["tag"]["id"]).first()
                      for t in i["post"]["tags"]])
        db.session.add(p)
    db.session.commit()

    print("Loading archives...")
    for i in data["archives"]:
        a = Archive.from_dict(i)
        db.session.add(a)
    db.session.commit()

    print("Loading topics...")
    for i in data["topics"]:
        t = Topic.from_dict(i)
        db.session.add(t)
    db.session.commit()

    print("Loading people...")
    for i in data["people"]:
        p = Person.from_dict(i)
        p.topics.extend([Topic.query.filter_by(id=t["topic"]["id"]).first()
                        for t in i["person"]["topics"]])
        db.session.add(p)
    db.session.commit()

    print("Loading boxes...")
    for i in data["boxes"]:
        b = Box.from_dict(i)
        b.archive = Archive.query.filter_by(id=i["box"]["archive"]["id"]).first()
        b.topics.extend([Topic.query.filter_by(id=t["topic"]["id"]).first()
                        for t in i["box"]["topics"]])
        db.session.add(b)
    db.session.commit()

    print("Loading documents...")
    for i in data["documents"]:
        d = Document.from_dict(i)
        d.box = Box.query.filter_by(id=i["document"]["box"]["id"]).first()
        d.authors.extend([Person.query.filter_by(id=p["person"]["id"]).first()
                         for p in i["document"]["authors"]])
        d.people.extend([Person.query.filter_by(id=p["person"]["id"]).first()
                        for p in i["document"]["people"]])
        b.topics.extend([Topic.query.filter_by(id=t["topic"]["id"]).first()
                        for t in i["document"]["topics"]])
    db.session.commit()

    print("Done!")


class ModelEventListeners():
    @staticmethod
    def on_update(target, value, oldvalue, initiator):
        target.last_update = datetime.utcnow()
