from kron.blueprints import api, make_api_get_response, make_api_get_list_response
from kron.models import Document
from kron.exceptions import APINotFound


@api.route("/documents/")
def get_documents():
    data = Document.query.all()
    if not data:
        raise APINotFound()
    return make_api_get_list_response(data)


@api.route("/documents/<int:id>")
def get_document(id):
    data = Document.query.filter_by(id=id).first()
    if not data:
        raise APINotFound()
    return make_api_get_response(data)