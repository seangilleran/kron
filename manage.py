from flask_script import Manager

from kron import create_app, db, models, blog_models


app = create_app()
manager = Manager(app)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.shell
def _make_shell_context():
    return dict(app=app, db=db, models=models, blog_models=blog_models)


if __name__ == "__main__":
    manager.run()
