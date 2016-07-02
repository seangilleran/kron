from datetime import datetime

from flask import jsonify, make_response, request

from kron import db
from kron.blueprints import api
from kron.models import Topic
from kron.exceptions import APIInvalidUsage, APINotFound


@api.route("/topics/")
def get_topics():
    """Get all Topics"""
    topics = Topic.query.all()
    if not topics:
        raise APINotFound()
    res = jsonify(dict(
        topics=[t.to_dict() for t in topics]
    ))
    res.headers["Location"] = topics[0].get_url()
    return res


@api.route("/topics/<name>")
def get_topic(name):
    """Get a specific topic by topic.name"""
    topic = Topic.query.filter_by(name=name).first()
    if not topic:
        raise APINotFound()
    res = jsonify(dict(
        topics=[topic.to_dict()]
    ))
    res.headers["Location"] = topic.get_url()
    return res
