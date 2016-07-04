from flask_script import Manager

from kron import Kron, db, restore_from_file
from kron import Tag, Post, Archive, Box, Document, Person, Topic


app = Kron(__name__)
manager = Manager(app)


@manager.command
def data(file):
    restore_from_file(file)


@manager.shell
def _make_shell_context():
    return dict(
        app=app, db=db, Tag=Tag, Post=Post,
        Archive=Archive, Box=Box, Document=Document, Person=Person,
        Topic=Topic
    )


if __name__ == "__main__":
    manager.run()
