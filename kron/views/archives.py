import flask
from flask_classy import FlaskView, route

from kron.db import db
import kron.utils as u
from kron.views.base import BaseView
from kron.models import Archive, Box


class ArchivesView(BaseView):
    resource = Archive

    @route('<id>/boxes/')
    def get_boxes(self, id):
        archive = u.find_or_404(Archive, id)
        rv = [dict(
            name=x.name, uri=x.get_uri()
        ) for x in archive.boxes]
        if not rv:
            return ('', 204)
        return u.make_res(rv, jsonify=True)

    @route('<id>/boxes/<boxid>')
    def get_box(self, id, boxid):
        return u.redirect(flask.url_for('BoxesView:get', id=boxid))

    @route('<id>/boxes/<boxid>', methods=['PUT'])
    def add_box(self, id, boxid):
        archive = u.find_or_404(Archive, id)
        box = u.find_or_404(Box, boxid)
        if box in archive.boxes:
            flask.abort(409)  # Already has this box.
        archive.boxes.append(box)
        archive.save()
        return ('', 204)

    @route('<id>/boxes/<boxid>', methods=['DELETE'])
    def remove_box(self, id, boxid):
        archive = u.find_or_404(Archive, id)
        box = u.find_or_404(Box, id)
        if box not in archive.boxes:
            flask.abort(415)  # Box not here, man.
        archive.boxes.remove(box)
        archive.save()
        return ('', 204)
