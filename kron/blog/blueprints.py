from flask import Blueprint, render_template, jsonify

import kron.blog.models as blog_models


blog = Blueprint("blog", __name__, template_folder="templates")


@blog.route("/")
def index():
    """Return front page template with a list of blog posts."""
    return render_template("index.html")


@blog.route("/api/blog/posts/")
def get_posts():
    posts = blog_models.Post.query.all()
    if not posts:
        abort(404)
    return jsonify({"posts": [p.to_dict() for p in posts]})


@blog.route("/api/blog/posts/<int:id>")
def get_post(id):
    post = blog_models.Post.query.get_or_404(id)
    return jsonify(post.to_dict())


@blog.route("/api/blog/tags/")
def get_tags():
    tags = blog_models.Tag.query.all()
    if not tags:
        abort(404)
    return jsonify({"tags": [t.to_dict() for t in tags]})


@blog.route("/api/blog/tags/<int:id>")
def get_tag(id):
    tag = blog_models.Tag.query.get_or_404(id)
    return jsonify(tag.to_dict())
