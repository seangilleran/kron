from flask import Blueprint, render_template

from kron.models import Archive, Box, Document, Person, Topic


kron = Blueprint("kron", __name__)


@kron.route("/archives/")
def get_archives():
    archives = Archive.query.all()
    return render_template("archives.htm", archives=archives)
