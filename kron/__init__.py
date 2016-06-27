import os
import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import kron.blueprints as blueprints


db = SQLAlchemy()


def create_app():
    """Create a new application instance."""
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=str(uuid.uuid4()),
        SQLALCHEMY_DATABASE_URI="sqlite:///kron_db.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    db.init_app(app)

    app.register_blueprint(blueprints.blog)

    return app
