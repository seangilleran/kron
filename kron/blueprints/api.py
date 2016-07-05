from flask import Blueprint

from kron.api import API
from kron.models import Archive, Box, Document, Person, Topic


api = Blueprint("api", __name__)


##
@api.route("/archives")
def get_archives():
    return API.query_all(Archive)


@api.route("/archives/<int:id>")
def get_archive(id):
    return API.query_by_id(Archive, id)


@api.route("/archives/", methods=["POST"])
def new_archive():
    return API.add_new(Archive, request.get_json())


@api.route("/archives/<int:id>", methods=["PUT"])
def update_archive(id):
    return API.update_by_id(Archive, request.get_json(), id)


@api.route("/archives/<int:id>", methods=["DELETE"])
def delete_archive(id):
    return API.delete_by_id(Archive, id)


##
@api.route("/boxes/")
def get_boxes():
    return API.query_all(Box)


@api.route("/boxes/<int:id>")
def get_box(id):
    return API.query_by_id(Box, id)


@api.route("/boxes/", methods=["POST"])
def new_box():
    return API.add_new(Box, request.get_json())


@api.route("/boxes/<int:id>", methods=["PUT"])
def update_box(id):
    return API.update_by_id(Box, request.get_json(), id)


@api.route("/boxes/<int:id>", methods=["DELETE"])
def delete_box(id):
    return API.delete_by_id(Box, id)


@api.route("/boxes/<int:id>/people")
def get_people_for_box(id):
    return API.get_people(Box, id)


@api.route("/boxes/<int:d_id>/people/<int:p_id>", methods=["POST"])
def add_person_to_box(d_id, p_id):
    return API.add_person(Box, d_id, p_id)


@api.route("/boxes/<int:d_id>/people/<int:p_id>", methods=["DELETE"])
def remove_person_from_box(d_id, p_id):
    return API.remove_person(Box, d_id, p_id)


@api.route("/boxes/<int:id>/topics")
def get_topics_for_box(id):
    return API.get_topics(Box, id)


@api.route("/boxes/<int:b_id>/topics/<int:t_id>", methods=["POST"])
def add_topic_to_box(b_id, t_id):
    return API.add_topic(Box, b_id, t_id)


@api.route("/boxes/<int:b_id>/topics/<int:t_id>", methods=["DELETE"])
def remove_topic_from_box(b_id, t_id):
    return API.remove_topic(Box, b_id, t_id)


##
@api.route("/documents/")
def get_documents():
    return API.query_all(Document)


@api.route("/documents/<int:id>")
def get_document(id):
    return API.query_by_id(Document, id)

@api.route("/documents/", methods=["POST"])
def new_document():
    return API.add_new(Document, request.get_json())


@api.route("/documents/<int:id>", methods=["PUT"])
def update_document(id):
    return API.update_by_id(Document, request.get_json(), id)


@api.route("/documents/<int:id>", methods=["DELETE"])
def delete_document(id):
    return API.delete_by_id(Document, id)


@api.route("/documents/<int:id>/authors")
def get_authors_for_document(id):
    return API.get_authors(Document, id)


@api.route("/documents/<int:d_id>/authors/<int:p_id>", methods=["POST"])
def add_author_to_document(d_id, p_id):
    return API.add_author(Document, d_id, p_id)


@api.route("/documents/<int:d_id>/authors/<int:p_id>", methods=["DELETE"])
def remove_author_from_document(d_id, p_id):
    return API.remove_author(Document, d_id, p_id)


@api.route("/documents/<int:id>/people")
def get_people_for_document(id):
    return API.get_people(Document, id)


@api.route("/documents/<int:d_id>/people/<int:p_id>", methods=["POST"])
def add_person_to_document(d_id, p_id):
    return API.add_person(Document, d_id, p_id)


@api.route("/documents/<int:d_id>/people/<int:p_id>", methods=["DELETE"])
def remove_person_from_document(d_id, p_id):
    return API.remove_person(Document, d_id, p_id)


@api.route("/documents/<int:id>/topics")
def get_topics_for_document(id):
    return API.get_topics(Document, id)


@api.route("/documents/<int:d_id>/topics/<int:t_id>", methods=["POST"])
def add_topic_to_document(d_id, t_id):
    return API.add_topic(Document, d_id, t_id)


@api.route("/documents/<int:d_id>/topics/<int:t_id>", methods=["DELETE"])
def remove_topic_from_document(d_id, t_id):
    return API.remove_topic(Document, d_id, t_id)


##
@api.route("/people/")
def get_people():
    return API.query_all(Person)


@api.route("/people/<int:id>")
def get_person(id):
    return API.query_by_id(Person, id)


@api.route("/people/", methods=["POST"])
def new_person():
    return API.add_new(Person, request.get_json())


@api.route("/people/<int:id>", methods=["PUT"])
def update_person(id):
    return API.update_by_id(Person, request.get_json(), id)


@api.route("/people/<int:id>", methods=["DELETE"])
def delete_person(id):
    return API.delete_by_id(Person, id)


@api.route("/people/<int:id>/topics")
def get_topics_for_person(id):
    return API.get_topics(Person, id)


@api.route("/people/<int:p_id>/topics/<int:t_id>", methods=["POST"])
def add_topic_to_person(p_id, t_id):
    return API.add_topic(Person, p_id, t_id)


@api.route("/people/<int:p_id>/topics/<int:t_id>", methods=["DELETE"])
def remove_topic_from_person(p_id, t_id):
    return API.remove_topic(Person, p_id, t_id)


##
@api.route("/topics/")
def get_topics():
    return API.query_all(Topic)


@api.route("/topics/<int:id>")
def get_topic(id):
    return API.query_by_id(Topic, id)


@api.route("/topics/", methods=["POST"])
def new_topic():
    return API.add_new(Topic, request.get_json())


@api.route("/topics/<int:id>", methods=["PUT"])
def update_topic(id):
    return API.update_by_id(Topic, request.get_json(), id)


@api.route("/topics/<int:id>", methods=["DELETE"])
def delete_topic(id):
    return API.delete_by_id(Topic, id)
