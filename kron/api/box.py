from kron.blueprints import api, make_api_get_response, make_api_get_list_response
from kron.models import Box
from kron.exceptions import APINotFound


@api.route("/boxes/")
def get_boxes():
    data = Box.query.all()
    if not data:
        raise APINotFound()
    return make_api_get_list_response(data)


@api.route("/boxes/<int:id>")
def get_box(id):
    data = Box.query.filter_by(id=id).first()
    if not data:
        raise APINotFound()
    return make_api_get_response(data)
