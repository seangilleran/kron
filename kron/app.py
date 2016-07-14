import os
import uuid

import flask

from kron.db import db
import kron.models as models
import kron.views as views


def create_app(*args, **kwargs):
    """"""

    app = flask.Flask(
        __name__,
        instance_relative_config=True,
        *args, **kwargs
    )

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
    app.config.update(
        SECRET_KEY=str(uuid.uuid4()),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI='sqlite:///{p}'.format(
            p=os.path.join(app.instance_path, 'data.sqlite'))
    )

    db.init_app(app)
    views.ArchivesView.register(app)
    views.BoxesView.register(app)

    return app


def get_shell_context(app):
    """"""

    return dict(
        app=app, db=db,
        Box=models.Box, Archive=models.Archive
    )
