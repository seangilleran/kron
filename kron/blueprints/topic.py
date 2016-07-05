from kron.blueprints import api
from kron.blueprints import make_api_get_response, make_api_get_list_response
from kron.blueprints import make_api_update_response
from kron.models import Topic
from kron.exceptions import APIInvalidUsage, APINotFound


@api.route("/topics/")
def get_topics():
    topics = Topic.query.all()
    if not topics:
        raise APINotFound()
    return make_api_get_list_response(topics)


@api.route("/topics/<int:id>")
def get_topic(id):
    topic = Topic.query.filter_by(id=id).first()
    if not topic:
        raise APINotFound()
    return make_api_get_response(topic)


@api.route("/topics/", methods=["POST"])
def new_topic():
    data = request.get_json()
    if not data:
        raise APIInvalidUsage("Missing or invalid data: topic")
    topic = Topic.from_dict(data)
    db.session.add(topic)
    db.session.commit()
    return make_api_update_response(topic, 201)


@api.route("/topics/<int:id>", methods=["PUT"])
def update_topic(id):
    data = request.get_json()
    if not data:
        raise APIInvalidUsage("Missing or invalid data: topic")
    topic = Topic.query.filter_by(id=id).first()
    if not topic:
        raise APINotFound()
    topic.update_from_dict(data)
    db.session.add(topic)
    db.session.commit()
    return make_api_update_response(topic)


@api.route("/topics/<int:id>", methods=["DELETE"])
def delete_topic(id):
    topic = Topic.query.filter_by(id=id).first()
    if not topic:
        raise APINotFound()
    db.session.delete(topic)
    db.session.commit()
    return ("", 204)
