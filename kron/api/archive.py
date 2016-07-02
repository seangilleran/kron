from datetime import datetime
from re import sub

from flask import jsonify, make_response, request

from kron import db
from kron.blueprints import api
from kron.models import Archive
from kron.exceptions import APIInvalidUsage, APINotFound


@api.route("/archives/")
def get_archives():
    """Get all Archives"""
    archives = Archive.query.all()
    if not archives:
        raise APINotFound()
    res = jsonify([a.to_dict() for a in archives])
    res.headers["Location"] = archives[0].get_url()
    return res


@api.route("/archives/<name>")
def get_archive(name):
    """Get a specific Archive by Archive.name"""
    name = name.replace("%20", "_")
    name = sub("[^A-Za-z]", "_", name)
    archive = Archive.query.filter_by(name=name).first()
    if not archive:
        raise APINotFound()
    res = jsonify(dict(
        archives=[archive.to_dict()]
    ))
    res.headers["Location"] = archive.get_url()
    return res


@api.route("/archives", methods=["POST", "PUT"])
def new_archive():
    """
    Add a new Archive with HTTP POST or PUT.

    {"Archive": {"name": "<Archive.name>"}}
    """
    data = request.get_json()
    if not data or not data.get("name"):
        raise APIInvalidUsage("Missing data: Archive.name")
    if len(data["name"]) >= 128:
        raise APIInvalidUsage("Archive.name must be < 128 char")
    archive = Archive(data["name"])
    db.session.add(archive)
    db.session.commit()
    res = make_response(jsonify(dict(
        message="Created {a}".format(a=archive),
        url=archive.get_url()
    )), 201)
    res.headers["Location"] = archive.get_url()
    return res


@api.route("/archives/<name>", methods=["PUT", "PATCH"])
def update_archive(name):
    """
    Update an Archive by Archive.name with HTTP PUT or PATCH.

    {"Archive": {"name": "<Archive.name>"}}
    """
    archive = Archive.query.filter_by(name=name).first()
    if not archive:
        raise APINotFound()
    data = request.get_json()
    if not data or not data.get("Archive"):
        raise APIInvalidUsage("Missing data: Archive")
    if not data["Archive"].get("name"):
        raise APIInvalidUsage("Missing data: Archive.name")
    if len(data["Archive"]["name"]) >= 128:
        raise APIInvalidUsage("Archive.name must be < 128 char")
    archive.full_name = data["Archive"]["name"]
    db.session.add(archive)
    db.session.commit()
    res = make_response(jsonify(dict(
        message="Updated {a}".format(a=archive),
        url=archive.get_url()
    )))
    res.headers["Location"] = archive.get_url()
    return res
