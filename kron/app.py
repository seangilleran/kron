import uuid

from flask import Flask


def create_app(db, blueprints=[]):
    """Create a new application instance."""
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=str(uuid.uuid4()),
        EXPLAIN_TEMPLATE_LOADING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///kron_data.sqlite",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    db.init_app(app)
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    return app
