from kron.blueprints import api, make_api_get_response, make_api_get_list_response
from kron.models import Archive
from kron.exceptions import APINotFound


@api.route("/archives/")
def get_archives():
    data = Archive.query.all()
    if not data:
        raise APINotFound()
    return make_api_get_list_response(data)


@api.route("/archives/<int:id>")
def get_archive(id):
    data = Archive.query.filter_by(id=id).first()
    if not data:
        raise APINotFound()
    return make_api_get_response(data)
