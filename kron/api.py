from flask import jsonify, make_response, render_template

from kron.db import db, is_ok
from kron.exceptions import APIInvalidUsage, APINotFound


def make_update_response(obj, code=200):
    res = make_response(jsonify(dict(
        message="Updated {o}".format(o=obj),
        url=obj.get_url()
    )), code)
    res.headers["Location"] = obj.get_url()
    return res


class API:
    @staticmethod
    def query_all(model):
        obj = model.query.all()
        if not is_ok(obj):
            raise APINotFound()
        res = make_response(jsonify(
            [o.to_dict() for o in obj]))
        res.headers["Location"] = obj[0].get_url()
        return res

    @staticmethod
    def query_by_id(model, id):
        obj = model.query.filter_by(id=id).first()
        if not is_ok(obj):
            raise APINotFound()
        res = make_response(jsonify(obj.to_dict()))
        res.headers["Location"] = obj.get_url()
        return res

    @staticmethod
    def add_new(model, data):
        if not is_ok(data):
            raise APIInvalidUsage("Missing or invalid data")
        obj = model.from_dict(data)
        db.session.add(obj)
        db.session.commit()
        return make_update_response(obj, 201)

    @staticmethod
    def update_by_id(model, data, id):
        if not is_ok(data):
            raise APIInvalidUsage("Missing or invalid data")
        obj = model.query.filter_by(id=id).first()
        if not is_ok(obj):
            raise APINotFound()
        obj.update_from_dict(data)
        db.session.add(obj)
        db.session.commit()
        return make_update_response(obj)

    @staticmethod
    def delete_by_id(model, id):
        obj = model.query.filter_by(id=id).first()
        if not is_ok(obj):
            raise APINotFound()
        db.session.delete(obj)
        db.session.commit()
        return("", 204)

    @staticmethod
    def get_people(model, id):
        obj = model.query.filter_by(id=id).first()
        if not obj or not obj.people:
            raise APINotFound()
        res = make_response(jsonify(
            [o.to_dict() for o in obj.people]))
        res.headers["Location"] = obj.people[0].get_url()
        return res

    @staticmethod
    def add_person(model, m_id, p_id):
        obj = model.query.filter_by(id=m_id).first()
        person = Person.query.filter_by(id=p_id).first()
        if not is_ok(obj) or not is_ok(person):
            raise APINotFound()
        if person in obj.people:
            raise APIInvalidUsage("Invalid data")
        obj.people.append(person)
        db.session.add(obj)
        db.session.commit()
        return make_update_response(obj)

    @staticmethod
    def remove_person(model, m_id, p_id):
        obj = model.query.filter_by(id=d_id).first()
        person = Person.query.filter_by(id=p_id).first()
        if not obj or not person:
            raise APINotFound()
        if person not in obj.people:
            raise APIInvalidUsage("Invalid data")
        obj.people.remove(person)
        db.session.add(obj)
        db.session.commit()
        return make_update_response(obj)

    @staticmethod
    def get_authors(model, id):
        obj = model.query.filter_by(id=id).first()
        if not obj or not obj.authors:
            raise APINotFound()
        res = make_response(jsonify(
            [o.to_dict() for o in obj.authors]))
        res.headers["Location"] = obj.authors[0].get_url()
        return res

    @staticmethod
    def add_author(model, m_id, p_id):
        obj = model.query.filter_by(id=m_id).first()
        author = Person.query.filter_by(id=p_id).first()
        if not is_ok(obj) or not is_ok(author):
            raise APINotFound()
        if author in obj.authors:
            raise APIInvalidUsage("Invalid data")
        obj.authors.append(author)
        db.session.add(obj)
        db.session.commit()
        return make_update_response(obj)

    @staticmethod
    def remove_author(model, m_id, p_id):
        obj = model.query.filter_by(id=d_id).first()
        author = Person.query.filter_by(id=p_id).first()
        if not obj or not author:
            raise APINotFound()
        if author not in obj.authors:
            raise APIInvalidUsage("Invalid data")
        obj.authors.remove(author)
        db.session.add(obj)
        db.session.commit()
        return make_update_response(obj)

    @staticmethod
    def get_topics(model, id):
        obj = model.query.filter_by(id=id).first()
        if not obj or not obj.topics:
            raise APINotFound()
        res = make_response(jsonify(
            [o.to_dict() for o in obj.topics]))
        res.headers["Location"] = obj.topics[0].get_url()
        return res

    @staticmethod
    def add_topic(model, m_id, t_id):
        obj = model.query.filter_by(id=m_id).first()
        topic = Topic.query.filter_by(id=t_id).first()
        if not is_ok(obj) or not is_ok(topic):
            raise APINotFound()
        if topic in obj.topics:
            raise APIInvalidUsage("Invalid data")
        obj.topics.append(topic)
        db.session.add(obj)
        db.session.commit()
        return make_update_response(obj)

    @staticmethod
    def remove_topic(model, m_id, t_id):
        obj = model.query.filter_by(id=d_id).first()
        topic = Topic.query.filter_by(id=t_id).first()
        if not obj or not topic:
            raise APINotFound()
        if topic not in obj.topics:
            raise APIInvalidUsage("Invalid data")
        obj.topics.remove(topic)
        db.session.add(obj)
        db.session.commit()
        return make_update_response(obj)
