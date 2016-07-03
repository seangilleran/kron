from flask_script import Manager

from kron import Kron, db
from kron import Archive, Box, Document, Person, Topic, Tag, Post


app = Kron(__name__)
manager = Manager(app)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def fake_data():
    db.drop_all()
    db.create_all()

    tags = [
        Tag(name="Cool"), Tag(name="Rad"), Tag(name="Sick"), Tag(name="Dope")
    ]
    db.session.add_all(tags)
    db.session.commit()

    p1 = Post(
        title="Duis quis congue odio, efficitur fermentum libero.",
        body="Ut ligula lacus, accumsan sed libero pulvinar, lobortis " +
             "mollis diam. Sed justo neque, sagittis id mattis in, " +
             "gravida eu turpis. Suspendisse potenti. Aliquam ut tempor " +
             "augue. Ut ut urna vulputate, varius tellus id, laoreet " +
             "dui. Cras tempus tincidunt ligula ac fringilla. Curabitur " +
             "non orci ut justo euismod imperdiet sit amet eu turpis."
    )
    p1.tags.extend([tags[0], tags[1]])
    p2 = Post(
        title="Cras at massa id libero tincidunt posuere.",
        body="Ut gravida vestibulum urna, id aliquet velit luctus nec. " +
             "Aenean efficitur volutpat quam vel condimentum. Praesent " +
             "ultrices non risus non elementum. Proin a placerat felis. " +
             "Duis felis nulla, dapibus eget diam sed, euismod facilisis " +
             "lorem. Maecenas ut lacinia sapien. Nunc magna leo, vehicula " +
             "ut sagittis ac, mattis eu diam. Phasellus semper sollicitudin " +
             "augue eu auctor. Nullam rutrum congue aliquam. Proin interdum " +
             "ex non euismod accumsan. Cras dapibus egestas ipsum ac " +
             "consequat. Nam vitae ante ac sem dapibus pellentesque nec at " +
             "risus. Nam auctor massa ipsum, ut finibus arcu suscipit sed. " +
             "Pellentesque sit amet augue faucibus, imperdiet tortor eu, " +
             "hendrerit eros."
    )
    p2.tags.extend([tags[0], tags[2], tags[3]])
    db.session.add_all([p1, p2])
    db.session.commit()
    print("Done!")



@manager.shell
def _make_shell_context():
    return dict(
        app=app, db=db, Tag=Tag, Post=Post,
        Archive=Archive, Box=Box, Document=Document, Person=Person,
        Topic=Topic
    )


if __name__ == "__main__":
    manager.run()
