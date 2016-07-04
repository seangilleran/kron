from flask import Blueprint, make_response, jsonify, render_template


api = Blueprint("api", __name__, template_folder="api/templates")


@api.route("/")
def get_kron_view():
    return render_template("kron.htm")


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
