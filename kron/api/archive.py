from flask import request

from kron.blueprints import (
    api, make_api_get_response, make_api_get_list_response,
    make_api_update_response)
from kron.models import Archive
from kron.exceptions import APIInvalidUsage, APINotFound


@api.route("/archives/")
def get_archives():
    archives = Archive.query.all()
    if not archives:
        raise APINotFound()
    return make_api_get_list_response(archives)


@api.route("/archives/<int:id>")
def get_archive(id):
    archive = Archive.query.filter_by(id=id).first()
    if not archive:
        raise APINotFound()
    return make_api_get_response(archive)


@api.route("/archives/", methods=["POST"])
def new_archive():
    data = request.get_json()
    if not data:
        raise APIInvalidUsage("Missing or invalid data: archive")
    archive = Archive.from_dict(data)
    db.session.add(archive)
    db.session.commit()
    return make_api_update_response(archive, 201)


@api.route("/archives/<int:id>", methods=["PUT"])
def update_archive(id):
    data = request.get_json()
    if not data:
        raise APIInvalidUsage("Missing or invalid data: archive")
    archive = Archive.query.filter_by(id=id).first()
    if not archive:
        raise APINotFound()
    archive.update_from_dict(data)
    db.session.add(archive)
    db.session.commit()
    return make_api_update_response(archive)


@api.route("/archives/<int:id>", methods=["DELETE"])
def delete_archive(id):
    archive = Archive.query.filter_by(id=id).first()
    if not archive:
        raise APINotFound()
    db.session.delete(archive)
    db.session.commit()
    return ("", 204)
