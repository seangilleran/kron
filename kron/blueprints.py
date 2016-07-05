from flask import Blueprint, render_template

from kron.models import Archive, Box, Document, Person, Topic


kron = Blueprint("kron", __name__)


@kron.route("/archives/")
def get_archives():
    archives = Archive.query.all()
    return render_template(
        "archives.htm", archives=archives,
        list=True
    )


@kron.route("/archives/<int:id>/")
@kron.route("/archives/<int:id>/<param>")
def get_archive(id, param=None):
    archive = Archive.query.get_or_404(id)
    return render_template(
        "archives.htm", archives=[archive],
        edit=archive.id if param == "edit" else None
    )


@kron.route("/boxes/")
def get_boxes():
    return "todo"


@kron.route("/boxes/<int:id>")
def get_box(id):
    return "todo"


@kron.route("/documents/")
def get_documents():
    return "todo"


@kron.route("/document/<int:id>")
def get_document(id):
    return "todo"


@kron.route("/people/")
def get_people():
    return "todo"


@kron.route("/people/<int:id>")
def get_person(id):
    return "todo"


@kron.route("/topics/")
def get_topics():
    return "todo"


@kron.route("/topics/<int:id>")
def get_topic(id):
    return "todo"
