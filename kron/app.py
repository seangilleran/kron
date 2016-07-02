from flask import Flask, make_response, jsonify

from kron import db, uniqid, exceptions
from kron.blog.blueprints import blog
from kron.blog.api import blog_api


class Kron(Flask):
    def __init__(self, name):
        Flask.__init__(self, name)

        self.config.from_pyfile("settings.cfg")

        db.init_app(self)

        self.register_blueprint(blog)
        self.register_blueprint(blog_api, url_prefix="/blog/api")

        @self.errorhandler(exceptions.APIInvalidUsage)
        @self.errorhandler(exceptions.APINotFound)
        def handle_api_exception(e):
            return make_response(jsonify(e.to_dict()), e.status_code)
