from kron.blueprints import api
from kron.blueprints import make_api_get_response, make_api_get_list_response
from kron.blueprints import make_api_update_response
from kron.models import Box
from kron.exceptions import APIInvalidUsage, APINotFound


@api.route("/boxes/")
def get_boxes():
    boxes = Box.query.all()
    if not boxes:
        raise APINotFound()
    return make_api_get_list_response(boxes)


@api.route("/boxes/<int:id>")
def get_box(id):
    box = Box.query.filter_by(id=id).first()
    if not box:
        raise APINotFound()
    return make_api_get_response(box)


@api.route("/boxes/", methods=["POST"])
def new_box():
    data = request.get_json()
    if not data:
        raise APIInvalidUsage("Missing or invalid data: box")
    box = Box.from_dict(data)
    db.session.add(box)
    db.session.commit()
    return make_api_update_response(box, 201)


@api.route("/boxes/<int:id>", methods=["PUT"])
def update_box(id):
    data = request.get_json()
    if not data:
        raise APIInvalidUsage("Missing or invalid data: box")
    box = Box.query.filter_by(id=id).first()
    if not box:
        raise APINotFound()
    box.update_from_dict(data)
    db.session.add(box)
    db.session.commit()
    return make_api_update_response(box)


@api.route("/boxes/<int:id>", methods=["DELETE"])
def delete_box(id):
    box = Box.query.filter_by(id=id).first()
    if not box:
        raise APINotFound()
    db.session.delete(box)
    db.session.commit()
    return ("", 204)


@api.route("/boxes/<int:id>/people")
def get_people_for_box(id):
    box = Box.query.filter_by(id=id).first()
    if not box or not box.people:
        raise APINotFound()
    return make_api_get_list_response(box.people)


@api.route("/boxes/<int:d_id>/people/<int:p_id>", methods=["POST"])
def add_person_to_box(d_id, p_id):
    box = Box.query.filter_by(id=d_id).first()
    person = Person.query.filter_by(id=p_id).first()
    if not box or not person:
        raise APINotFound()
    if person in box.people:
        raise APIInvalidUsage("Invalid data: box.people.person")
    box.people.append(person)
    db.session.add(box)
    db.session.commit()
    return make_api_update_response(box)


@api.route("/boxes/<int:d_id>/people/<int:p_id>", methods=["DELETE"])
def remove_person_from_box(d_id, p_id):
    box = Box.query.filter_by(id=d_id).first()
    person = Person.query.filter_by(id=p_id).first()
    if not box or not person:
        raise APINotFound()
    if person not in box.people:
        raise APIInvalidUsage("Invalid data: box.people.person")
    box.people.remove(person)
    db.session.add(box)
    db.session.commit()
    return make_api_update_response(box)


@api.route("/boxes/<int:id>/topics")
def get_topics_for_box(id):
    box = Box.query.filter_by(id=id).first()
    if not box or not box.topics:
        raise APINotFound()
    return make_api_get_list_response(box.topics)


@api.route("/boxes/<int:b_id>/topics/<int:t_id>", methods=["POST"])
def add_topic_to_box(b_id, t_id):
    box = Box.query.filter_by(id=b_id).first()
    topic = Topic.query.filter_by(id=t_id).first()
    if not box or not topic:
        raise APINotFound()
    if topic in box.topics:
        raise APIInvalidUsage("Invalid data: box.topics.topic")
    box.topics.append(topic)
    db.session.add(box)
    db.session.commit()
    return make_api_update_response(box)


@api.route("/boxes/<int:b_id>/topics/<int:t_id>", methods=["DELETE"])
def remove_topic_from_box(b_id, t_id):
    box = Box.query.filter_by(id=b_id).first()
    topic = Topic.query.filter_by(id=t_id).first()
    if not box or not topic:
        raise APINotFound()
    if topic not in box.topics:
        raise APIInvalidUsage("Invalid data: box.topics.topic")
    box.topics.remove(topic)
    db.session.add(box)
    db.session.commit()
    return make_api_update_response(box)
