import flask
from flask_classy import FlaskView

from kron.db import db
import kron.utils as u


class BaseView(FlaskView):
    """Contains basic CRUD operations for all resources."""
    resource = None

    def index(self):
        rv = [dict(
            name=x.name, uri=x.get_uri()
        ) for x in self.resource.query.all()]
        if not rv:
            return ('', 204)
        return u.make_res(rv, jsonify=True)

    def get(self, id):
        x = u.find_or_404(self.resource, id)
        if u.use_cached(self.resource, flask.request.headers):
            return('', 304)
        return u.make_res(
            payload=x.to_dict(),
            headers={'Last-Modified': x.last_modified},
            jsonify=True
        )

    def post(self):
        data = u.get_json_payload(flask.request)
        if self.resource.query.filter_by(name=data['name']).first():
            flask.abort(409)  # Already exists.
        x = self.resource.from_dict(data)
        x.save()
        return u.make_res('', {'Location': x.get_uri()}, 201)

    def put(self, id):
        x = u.find_or_404(self.resource, id)
        data = u.get_json_payload(flask.request)

        if self.resource.query.filter_by(name=data['name']).first():
            flask.abort(409)  # Already exists.
        if data['name'] == x.name:
            return ('', 304)  # Nothing changed!
        x.name = data['name']
        x.save()

        return ('', 204)

    def delete(self, id):
        x = u.find_or_404(self.resource, id)
        x.delete()
        return ('', 204)
