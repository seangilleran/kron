import flask
from flask_classy import FlaskView

from kron.models.box import Box


class BoxesView(FlaskView):
    """"""

    def index(self):
        rv = [b.to_dict() for b in Box.query.all()]
        return flask.jsonify(rv)

    def get(self, id):
        rv = Box.query.filter_by(id_hash=id).first()
        if not rv:
            flask.abort(404)
        return flask.jsonify(rv.to_dict())

