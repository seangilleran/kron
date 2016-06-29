import flask

from kron import db
import kron.blog.models as blog_models


blog_api = flask.Blueprint("blog_api", __name__)


@blog_api.route("/posts/")
def get_posts():
    posts = blog_models.Post.all_to_dict()
    if not posts:
        abort(404)
    return flask.jsonify(posts)


@blog_api.route("/posts/<int:id>")
def get_post(id):
    post = blog_models.Post.query.get_or_404(id)
    return flask.jsonify(post.to_dict())


@blog_api.route("/posts/", methods=["POST"])
def new_post():
    post = blog_models.Post.from_dict(flask.request.get_json())
    db.session.add(post)
    db.session.commit()
    return flask.jsonify(post.to_dict())


@blog_api.route("/tags/")
def get_tags():
    return flask.jsonify(blog_models.Tag.to_dict())


@blog_api.route("/tags/<int:id>")
def get_tag(id):
    tags = blog_models.Tag.all_to_dict()
    if not tags:
        flask.abort(404)
    return flask.jsonify(tags)


@blog_api.route("/tags/", methods=["POST"])
def new_tag():
    tag = blog_models.Tag.from_dict(flask.request.get_json())
    db.session.add(tag)
    db.session.commit()
    return flask.jsonify(tag.to_dict())
