from flask import Blueprint, make_response, jsonify

api = Blueprint("api", __name__)


def make_api_get_response(obj, code=200):
    res = make_response(jsonify(obj.to_dict()), code)
    res.headers["Location"] = obj.get_url()
    return res


def make_api_get_list_response(obj, code=200):
    res = make_response(jsonify(
        [o.to_dict() for o in obj]), code)
    res.headers["Location"] = obj[0].get_url()
    return res


def make_api_update_response(obj, code=200):
    res = make_response(jsonify(dict(
        message="Updated {o}".format(o=obj),
        url=obj.get_url()
    )), code)
    res.headers["Location"] = obj.get_url()
    return res


from kron.api import *
