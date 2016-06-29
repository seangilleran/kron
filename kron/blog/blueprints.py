from flask import Blueprint, render_template, request, jsonify

from kron import db
import kron.blog.models as blog_models


blog = Blueprint("blog", __name__, template_folder="templates")


@blog.route("/")
def index():
    """Return front page template with a list of blog posts."""
    return render_template("index.html")


@blog.route("/api/blog/posts/")
def get_posts():
    posts = blog_models.Post.all_to_dict()
    if not posts:
        abort(404)
    return jsonify(posts)


@blog.route("/api/blog/posts/<int:id>")
def get_post(id):
    post = blog_models.Post.query.get_or_404(id)
    return jsonify(post.to_dict())


@blog.route("/api/blog/posts/", methods=["POST"])
def new_post():
    post = blog_models.Post.from_json(request.get_json())
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_dict())


@blog.route("/api/blog/tags/")
def get_tags():
    return jsonify(blog_models.Tag.to_dict())


@blog.route("/api/blog/tags/<int:id>")
def get_tag(id):
    tags = blog_models.Tag.all_to_dict()
    if not tags:
        abort(404)
    return jsonify(tags)
