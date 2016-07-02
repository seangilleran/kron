from datetime import datetime

from flask import jsonify, make_response, request

from kron import db
from kron.blueprints import api
from kron.models import Document
from kron.exceptions import APIInvalidUsage, APINotFound


@api.route("/documents/")
def get_documents():
    """Get all Documents"""
    documents = Document.query.all()
    if not documents:
        raise APINotFound()
    res = jsonify(dict(
        documents=[d.to_dict() for d in documents]
    ))
    res.headers["Location"] = documents[0].get_url()
    return res


@api.route("/documents/<id>")
def get_document(id):
    """Get a specific Document by Document.id"""
    document = Document.query.filter_by(id=id).first()
    if not document:
        raise APINotFound()
    res = jsonify(dict(
        documents=[document.to_dict()]
    ))
    res.headers["Location"] = document.get_url()
    return res
