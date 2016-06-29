import flask

from kron import db
import kron.blog.models as blog_models


blog = flask.Blueprint("blog", __name__, template_folder="templates")


@blog.route("/")
def index():
    return flask.render_template("index.html")
