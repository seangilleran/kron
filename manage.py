from flask_script import Manager

from kron import Kron, db, models, Tag, Post


app = Kron(__name__)
manager = Manager(app)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.shell
def _make_shell_context():
    return dict(
        app=app, db=db, models=models,
        Tag=Tag, Post=Post
    )


if __name__ == "__main__":
    manager.run()
