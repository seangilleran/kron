import uuid

from flask import Flask, make_response, jsonify

from kron import db
import kron.exceptions
from kron.blog.blueprints import blog
from kron.blog.api import blog_api


def create_app():
    """Create a new application instance."""
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=str(uuid.uuid4()),
        SQLALCHEMY_DATABASE_URI="sqlite:///kron_data.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    db.init_app(app)
    app.register_blueprint(blog)
    app.register_blueprint(blog_api, url_prefix="/blog/api")

    @app.errorhandler(kron.exceptions.APIInvalidUsage)
    @app.errorhandler(kron.exceptions.APINotFound)
    def handle_api_exception(e):
        return make_response(jsonify(e.to_dict()), e.status_code)

    return app
