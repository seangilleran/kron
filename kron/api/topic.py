from kron.blueprints import api, make_api_get_response, make_api_get_list_response
from kron.models import Topic
from kron.exceptions import APINotFound


@api.route("/topics/")
def get_topics():
    data = Topic.query.all()
    if not data:
        raise APINotFound()
    return make_api_get_list_response(data)


@api.route("/topics/<int:id>")
def get_topic(id):
    data = Topic.query.filter_by(id=id).first()
    if not data:
        raise APINotFound()
    return make_api_get_response(data)
