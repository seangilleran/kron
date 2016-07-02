from datetime import datetime

from flask import Blueprint, abort, jsonify, make_response, request

from kron import db
from kron.exceptions import APIInvalidUsage, APINotFound
from kron.blog.models import Tag, Post


blog_api = Blueprint("blog_api", __name__)


@blog_api.route("/posts/")
def get_posts():
    """Get all Posts"""
    posts = Post.query.all()
    if not posts:
        raise APINotFound()
    return jsonify(dict(
        posts=[p.to_dict() for p in posts]
    ))


@blog_api.route("/posts/<int:id>")
def get_post(id):
    """Get a specific Post by Post.id"""
    post = Post.query.filter_by(id=id).first()
    if not post:
        raise APINotFound()
    return jsonify(dict(
        posts=[post.to_dict()]
    ))


@blog_api.route("/posts/", methods=["POST"])
def new_post():
    """Create a new Post or set of Posts"""
    data = request.get_json()
    if not data or not data.get("posts"):
        raise APIInvalidUsage("Missing posts data")
    posts = []
    for p in data["posts"]:
        if not p.get("title") or len(p["title"]) >= 128:
            raise APIInvalidUsage("Missing title or title too long")
        if not p.get("body"):
            raise APIInvalidUsage("Missing body")
        post = Post(title=p["title"], body=p["body"])
        if p.get("tags"):
            for t in p["tags"]:
                tag = Tag.query.filter_by(name=t).first()
                if not tag:
                    raise APIInvalidUsage("No such tag: " + t)
                post.tags.append(tag)
        post.timestamp = datetime.now()
        posts.append(post)
    db.session.add_all(posts)
    db.session.commit()
    res = make_response(jsonify(dict(
        message="Created {n} posts".format(n=len(posts)),
        posts=[p.get_url() for p in posts]
    )), 201)
    res.headers["Location"] = posts[0].get_url()
    return res


@blog_api.route("/posts/<int:id>/tags", methods=["PUT"])
def add_tags_to_post(id):
    """Add a set of Tags to a Post.tags by Post.id"""
    post = Post.query.filter_by(id=id).first()
    if not post:
        raise APINotFound()
    data = request.get_json()
    if not data or not data.get("tags"):
        raise APIInvalidUsage("Missing tags data")
    tags = []
    for t in data["tags"]:
        tag = Tag.query.filter_by(name=t).first()
        if not tag:
            raise APIInvalidUsage("No such tag: " + t)
        if tag not in post.tags:
            tags.append(tag)
            post.tags.append(tag)
    db.session.add(post)
    db.session.commit()
    res = make_response(jsonify(dict(
        message="Added {n} tags to {p}".format(n=len(tags), p=post),
        post=post.get_url()
    )))
    res.headers["Location"]=post.get_url()
    return res


@blog_api.route("/posts/<int:id>/tags", methods=["DELETE"])
def remove_tags_from_post(id):
    """Remove a set of Tags from a Post.tags by Post.id"""
    post = Post.query.filter_by(id=id).first()
    if not post:
        raise APINotFound()
    data = request.get_json()
    if not data or not data.get("tags"):
        raise APIInvalidUsage("Missing tags data")
    tags = []
    for t in data["tags"]:
        tag = Tag.query.filter_by(name=t).first()
        if not tag:
            raise APIInvalidUsage("No such tag: " + t)
        if tag in post.tags:
            tags.append(tag)
            post.tags.remove(tag)
    db.session.add(post)
    db.session.commit()
    res = make_response(jsonify(dict(
        message="Removed {n} tags from {p}".format(n=len(tags), p=post),
        post=post.get_url()
    )))
    res.headers["Location"]=post.get_url()
    return res


@blog_api.route("/posts/<int:id>", methods=["PUT"])
def update_post(id):
    """Update a Post by Post.id"""
    post = Post.query.filter_by(id=id).first()
    if not post:
        raise APINotFound()
    data = request.get_json()
    if data.get("title"):
        if len(data["title"]) >= 128:
            raise APIInvalidUsage("Title too long")
        post.title = data["title"]
    if data.get("body"):
        post.body = body
    db.session.add(post)
    db.session.commit()
    res = make_response(jsonify(dict(
        message="Updated post {n}".format(n=post.id),
        post=post.get_url()
    )))
    res.headers["Location"] = post.get_url()
    return res


@blog_api.route("/posts/<int:id>", methods=["DELETE"])
def delete_post(id):
    """Delete a Post by Post.id"""
    post = Post.query.filter_by(id=id).first()
    if not post:
        raise APINotFound()
    db.session.delete(post)
    db.session.commit()
    return ("", 204)


@blog_api.route("/tags/")
def get_tags():
    tags = Tag.query.all()
    if not tags:
        raise APINotFound()
    return jsonify(dict(
        tags=[t.to_dict() for t in tags]
    ))


@blog_api.route("/tags/<name>")
def get_tag(name):
    tag = Tag.query.filter_by(name=name).first()
    if not tag:
        raise APINotFound()
    return jsonify(dict(
        tags=[tag.to_dict()]
    ))


@blog_api.route("/tags/", methods=["POST"])
def new_tag():
    data = request.get_json()
    if not data or not data.get("tags"):
        raise APIInvalidUsage("Missing tags data")
    tags = []
    for t in data["tags"]:
        if not t.get("name") or len(t["name"]) >= 64:
            raise APIInvalidUsage("Missing name or name too long")
        if Tag.query.filter_by(name=t["name"]).first():
            raise APIInvalidUsage("Tag already exists: " + t["name"])
        tags.append(Tag(name=t["name"]))
    db.session.add_all(tags)
    db.session.commit()
    res=make_response(jsonify(dict(
        message="Created {n} tags".format(n=len(tags)),
        tags=[t.get_url() for t in tags]
    )), 201)
    res.headers["Location"]=tags[0].get_url()
    return res


@blog_api.route("/tags/<name>", methods=["DELETE"])
def delete_tag(name):
    tag = Tag.query.filter_by(name=name).first()
    if not tag:
        raise APINotFound()
    db.session.delete(tag)
    db.session.commit()
    return ("", 204)
