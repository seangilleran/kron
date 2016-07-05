from kron.blueprints import api
from kron.blueprints import make_api_get_response, make_api_get_list_response
from kron.blueprints import make_api_update_response
from kron.models import Person
from kron.exceptions import APIInvalidUsage, APINotFound

@api.route("/people/")
def get_people():
    people = Person.query.all()
    if not people:
        raise APINotFound()
    return make_api_get_list_response(people)


@api.route("/people/<int:id>")
def get_person(id):
    person = Person.query.filter_by(id=id).first()
    if not person:
        raise APINotFound()
    return make_api_get_response(person)


@api.route("/people/", methods=["POST"])
def new_person():
    data = request.get_json()
    if not data:
        raise APIInvalidUsage("Missing or invalid data: person")
    person = Person.from_dict(data)
    db.session.add(person)
    db.session.commit()
    return make_api_update_response(person, 201)


@api.route("/people/<int:id>", methods=["PUT"])
def update_person(id):
    data = request.get_json()
    if not data:
        raise APIInvalidUsage("Missing or invalid data: person")
    person = Person.query.filter_by(id=id).first()
    if not person:
        raise APINotFound()
    person.update_from_dict(data)
    db.session.add(person)
    db.session.commit()
    return make_api_update_response(person)


@api.route("/people/<int:id>", methods=["DELETE"])
def delete_person(id):
    person = Person.query.filter_by(id=id).first()
    if not person:
        raise APINotFound()
    db.session.delete(person)
    db.session.commit()
    return ("", 204)


@api.route("/people/<int:id>/topics")
def get_topics_for_person(id):
    person = Person.query.filter_by(id=id).first()
    if not person or not person.topics:
        raise APINotFound()
    return make_api_get_list_response(person.topics)


@api.route("/people/<int:p_id>/topics/<int:t_id>", methods=["POST"])
def add_topic_to_person(p_id, t_id):
    person = Person.query.filter_by(id=p_id).first()
    topic = Topic.query.filter_by(id=t_id).first()
    if not person or not topic:
        raise APINotFound()
    if topic in person.topics:
        raise APIInvalidUsage("Invalid data: person.topics.topic")
    person.topics.append(topic)
    db.session.add(person)
    db.session.commit()
    return make_api_update_response(person)


@api.route("/people/<int:p_id>/topics/<int:t_id>", methods=["DELETE"])
def remove_topic_from_person(p_id, t_id):
    person = Person.query.filter_by(id=p_id).first()
    topic = Topic.query.filter_by(id=t_id).first()
    if not person or not topic:
        raise APINotFound()
    if topic not in person.topics:
        raise APIInvalidUsage("Invalid data: person.topics.topic")
    person.topics.remove(topic)
    db.session.add(person)
    db.session.commit()
    return make_api_update_response(person)
