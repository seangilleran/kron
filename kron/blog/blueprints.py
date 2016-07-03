import flask

from kron import db
from kron.blog.models import Tag, Post


blog = flask.Blueprint("blog", __name__, template_folder="templates")


@blog.route("/")
def get_posts():
    posts = Post.query.all()
    return flask.render_template(
        "posts.htm",
        posts=posts, pg="blog"
    )


@blog.route("/cv/")
def get_cv():
    return flask.render_template(
        "cv.htm",
        pg="cv"
    )


@blog.route("/projects/")
def get_projects():
    return flask.render_template(
        "projects.htm",
        pg="projects"
    )


@blog.route("/research/")
def get_research():
    return flask.render_template(
        "research.htm",
        pg="research"
    )


@blog.route("/posts/<title>")
def get_post(title):
    post = Post.query.filter_by(title=title).first()
    if not post:
        flask.abort(404)
    posts = [post]
    return flask.render_template(
        "post_by_name.htm",
        pg="blog", posts=posts
    )


@blog.route("/tags/<name>")
def get_tag(name):
    tag = Tag.query.filter_by(name=name).first()
    if not tag:
        flask.abort(404)
    posts = []
    for p in Post.query.all():
        if tag in p.tags:
            posts.append(p)
    return flask.render_template(
        "posts_by_tag.htm",
        pg="blog", posts=posts, tag=tag
    )
