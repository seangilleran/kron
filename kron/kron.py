from datetime import datetime
import os

from flask import Flask

from kron.db import db, moment
from kron.blueprints import kron as kron_bp
from kron.blog.blueprints import blog as blog_bp


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
                jquery_1_js=self.config["JQUERY_1_JS"],
                font_awesome_css=self.config["FONT_AWESOME_CSS"]
            )

        @self.context_processor
        def inject_time():
            return dict(
                timestamp=datetime.utcnow()
            )

        self.register_blueprint(blog_bp)
        self.register_blueprint(kron_bp, url_prefix="/kron")
