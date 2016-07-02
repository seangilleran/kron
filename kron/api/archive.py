from datetime import datetime

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
    res = jsonify(dict(
        archives=[a.to_dict() for a in archives]
    ))
    res.headers["Location"] = archives[0].get_url()
    return res


@api.route("/archives/<name>")
def get_archive(name):
    """Get a specific Archive by Archive.name"""
    archive = Archive.query.filter_by(name=name).first()
    if not archive:
        raise APINotFound()
    res = jsonify(dict(
        archives=[archive.to_dict()]
    ))
    res.headers["Location"] = archive.get_url()
    return res
