from datetime import datetime
import os

from flask import Flask, make_response, jsonify

from kron.db import db, moment
from kron.exceptions import APIInvalidUsage, APINotFound
import kron.blueprints as bp
import kron.blog.blueprints as blog_bp


class Kron(Flask):
    def __init__(self, name):
        Flask.__init__(self, name, static_url_path="")
        self.config.from_pyfile("settings.cfg")
        self.root_path = os.path.join(self.root_path, "kron")
        db.init_app(self)
        moment.init_app(self)

        @self.context_processor
        def inject_cdns():
            return dict(
                bootstrap_css=self.config["BOOTSTRAP_CSS"],
                bootstrap_js=self.config["BOOTSTRAP_JS"],
                jquery_3_js=self.config["JQUERY_3_JS"],
                jquery_2_js=self.config["JQUERY_2_JS"],
                jquery_1_js=self.config["JQUERY_1_JS"],
                angular_js=self.config["ANGULAR_JS"],
                font_awesome_css=self.config["FONT_AWESOME_CSS"]
            )

        @self.context_processor
        def inject_time():
            return dict(
                timestamp=datetime.utcnow()
            )

        self.register_blueprint(bp.kron, url_prefix="/kron")
        self.register_blueprint(bp.api, url_prefix="/kron/api")
        self.register_blueprint(blog_bp.blog)

        @self.errorhandler(APIInvalidUsage)
        @self.errorhandler(APINotFound)
        def handle_api_exception(e):
            return make_response(jsonify(e.to_dict()), e.status_code)
