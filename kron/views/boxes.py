import flask
from flask_classy import FlaskView, route

from kron.db import db
import kron.utils as u
from kron.views.base import BaseView
from kron.models import Box, Archive


class BoxesView(BaseView):
    resource = Box

    @route('<id>/archive/')
    def get_box_archive(self, id):
        box = u.find_or_404(Box, id)
        return u.redirect(box.archive.get_uri())

    @route('<id>/archive/<archiveid>')
    def get_archive(self, id, archiveid):
        return u.redirect(flask.url_for('ArchivesView:get', id=archiveid))

    @route('<id>/archive/<archiveid>', methods=['PUT'])
    def change_archive(self, id, archiveid):
        box = u.find_or_404(Box, id)
        if box.archive.id_hash == archiveid:
            flask.abort(409)  # Already part of this archive.
        archive = u.find_or_404(Archive, archiveid)
        box.archive = archive
        box.save()
        return ('', 204)
