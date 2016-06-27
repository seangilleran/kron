import flask

import kron.blog.models as models


blog = flask.Blueprint("blog", __name__, template_folder="templates")


@blog.route("/")
def index():
    """Return front page template with a list of blog posts."""
    return flask.render_template("index.html")
