from datetime import datetime

from flask import jsonify, make_response, request

from kron import db
from kron.blueprints import api
from kron.models import Person
from kron.exceptions import APIInvalidUsage, APINotFound


@api.route("/people/")
def get_people():
    """Get all people"""
    people = Person.query.all()
    if not people:
        raise APINotFound()
    res = jsonify(dict(
        people=[p.to_dict() for p in people]
    ))
    res.headers["Location"] = people[0].get_url()
    return res


@api.route("/people/<name>")
def get_person(name):
    """Get a specific Person by Person.name"""
    person = Person.query.filter_by(name=name).first()
    if not person:
        raise APINotFound()
    res = jsonify(dict(
        people=[person.to_dict()]
    ))
    res.headers["Location"] = person.get_url()
    return res
