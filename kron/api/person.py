from kron.blueprints import api, make_api_get_response, make_api_get_list_response
from kron.models import Person
from kron.exceptions import APINotFound


@api.route("/people/")
def get_people():
    data = Person.query.all()
    if not data:
        raise APINotFound()
    return make_api_get_list_response(data)


@api.route("/people/<int:id>")
def get_person(id):
    data = Person.query.filter_by(id=id).first()
    if not data:
        raise APINotFound()
    return make_api_get_response(data)
