import uuid

from flask import Flask

from kron import db
import kron.blog.blueprints as blog_blueprints


def create_app():
    """Create a new application instance."""
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=str(uuid.uuid4()),
        SQLALCHEMY_DATABASE_URI="sqlite:///kron_data.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    db.init_app(app)
    app.register_blueprint(blog_blueprints.blog)
    return app
