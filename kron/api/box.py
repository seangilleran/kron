from datetime import datetime

from flask import jsonify, make_response, request

from kron import db
from kron.blueprints import api
from kron.models import Box
from kron.exceptions import APIInvalidUsage, APINotFound


@api.route("/boxes/")
def boxes():
    """Get all Boxes"""
    boxes = Box.query.all()
    if not boxes:
        raise APINotFound()
    res = jsonify(dict(
        boxes=[b.to_dict() for b in boxes]
    ))
    res.headers["Location"] = boxes[0].get_url()
    return res


@api.route("/boxes/<number>")
def get_box(number):
    """Get a specific Box by Box.number"""
    box = Box.query.filter_by(number=number).first()
    if not box:
        raise APINotFound()
    res = jsonify(dict(
        boxes=[box.to_dict()]
    ))
    res.headers["Location"] = box.get_url()
    return res
