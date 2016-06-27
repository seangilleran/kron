import flask


blog = flask.Blueprint("blog", __name__)


@blog.route("/")
def index():
    return "Hey! Ho!"
