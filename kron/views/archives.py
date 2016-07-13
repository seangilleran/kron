import flask
from flask_classy import FlaskView, route

from kron.models.archive import Archive


class ArchivesView(FlaskView):
    """"""

    def index(self):
        rv = [a.to_dict() for a in Archive.query.all()]
        return flask.jsonify(rv)

    def get(self, id):
        rv = Archive.query.filter_by(id_hash=id).first()
        if not rv:
            flask.abort(404)
        return flask.jsonify(rv.to_dict())

    @route('/<id>/boxes/')
    def get_boxes(self, id):
        a = Archive.query.filter_by(id_hash=id).first()
        if not a or not a.boxes:
            flask.abort(404)
        rv = [b.to_dict() for b in a.boxes]
        return flask.jsonify(rv)

