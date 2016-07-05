from kron.blueprints import api
from kron.blueprints import make_api_get_response, make_api_get_list_response
from kron.blueprints import make_api_update_response
from kron.models import Document
from kron.exceptions import APIInvalidUsage, APINotFound


@api.route("/documents/")
def get_documents():
    documents = Document.query.all()
    if not documents:
        raise APINotFound()
    return make_api_get_list_response(documents)


@api.route("/documents/<int:id>")
def get_document(id):
    document = Document.query.filter_by(id=id).first()
    if not document:
        raise APINotFound()
    return make_api_get_response(document)


@api.route("/documents/", methods=["POST"])
def new_document():
    data = request.get_json()
    if not data:
        raise APIInvalidUsage("Missing or invalid data: document")
    document = Document.from_dict(data)
    db.session.add(document)
    db.session.commit()
    return make_api_update_response(document, 201)


@api.route("/documents/<int:id>", methods=["PUT"])
def update_document(id):
    data = request.get_json()
    if not data:
        raise APIInvalidUsage("Missing or invalid data: document")
    document = Document.query.filter_by(id=id).first()
    if not document:
        raise APINotFound()
    document.update_from_dict(data)
    db.session.add(document)
    db.session.commit()
    return make_api_update_response(document)


@api.route("/documents/<int:id>", methods=["DELETE"])
def delete_document(id):
    document = Document.query.filter_by(id=id).first()
    if not document:
        raise APINotFound()
    db.session.delete(document)
    db.session.commit()
    return ("", 204)


@api.route("/documents/<int:id>/authors")
def get_authors_for_document(id):
    document = Document.query.filter_by(id=id).first()
    if not document or not document.authors:
        raise APINotFound()
    return make_api_get_list_response(document.authors)


@api.route("/documents/<int:d_id>/authors/<int:p_id>", methods=["POST"])
def add_author_to_document(d_id, p_id):
    document = Document.query.filter_by(id=d_id).first()
    author = Person.query.filter_by(id=p_id).first()
    if not document or not author:
        raise APINotFound()
    if author in document.authors:
        raise APIInvalidUsage("Invalid data: document.authors.author")
    document.authors.append(author)
    db.session.add(document)
    db.session.commit()
    return make_api_update_response(document)


@api.route("/documents/<int:d_id>/authors/<int:p_id>", methods=["DELETE"])
def remove_author_from_document(d_id, p_id):
    document = Document.query.filter_by(id=d_id).first()
    author = Person.query.filter_by(id=p_id).first()
    if not document or not author:
        raise APINotFound()
    if author not in document.authors:
        raise APIInvalidUsage("Invalid data: document.authors.author")
    document.authors.remove(author)
    db.session.add(document)
    db.session.commit()
    return make_api_update_response(document)


@api.route("/documents/<int:id>/people")
def get_people_for_document(id):
    document = Document.query.filter_by(id=id).first()
    if not document or not document.people:
        raise APINotFound()
    return make_api_get_list_response(document.people)


@api.route("/documents/<int:d_id>/people/<int:p_id>", methods=["POST"])
def add_person_to_document(d_id, p_id):
    document = Document.query.filter_by(id=d_id).first()
    person = Person.query.filter_by(id=p_id).first()
    if not document or not person:
        raise APINotFound()
    if person in document.people:
        raise APIInvalidUsage("Invalid data: document.people.person")
    document.people.append(person)
    db.session.add(document)
    db.session.commit()
    return make_api_update_response(document)


@api.route("/documents/<int:d_id>/people/<int:p_id>", methods=["DELETE"])
def remove_person_from_document(d_id, p_id):
    document = Document.query.filter_by(id=d_id).first()
    person = Person.query.filter_by(id=p_id).first()
    if not document or not person:
        raise APINotFound()
    if person not in document.people:
        raise APIInvalidUsage("Invalid data: document.people.person")
    document.people.remove(person)
    db.session.add(document)
    db.session.commit()
    return make_api_update_response(document)


@api.route("/documents/<int:id>/topics")
def get_topics_for_document(id):
    document = Document.query.filter_by(id=id).first()
    if not document or not document.topics:
        raise APINotFound()
    return make_api_get_list_response(document.topics)


@api.route("/documents/<int:d_id>/topics/<int:t_id>", methods=["POST"])
def add_topic_to_document(d_id, t_id):
    document = Document.query.filter_by(id=d_id).first()
    topic = Topic.query.filter_by(id=t_id).first()
    if not document or not topic:
        raise APINotFound()
    if topic in document.topics:
        raise APIInvalidUsage("Invalid data: document.topics.topic")
    document.topics.append(topic)
    db.session.add(document)
    db.session.commit()
    return make_api_update_response(document)


@api.route("/documents/<int:d_id>/topics/<int:t_id>", methods=["DELETE"])
def remove_topic_from_document(d_id, t_id):
    document = Document.query.filter_by(id=d_id).first()
    topic = Topic.query.filter_by(id=t_id).first()
    if not document or not topic:
        raise APINotFound()
    if topic not in document.topics:
        raise APIInvalidUsage("Invalid data: document.topics.topic")
    document.topics.remove(topic)
    db.session.add(document)
    db.session.commit()
    return make_api_update_response(document)
