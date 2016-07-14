from flask_script import Manager

import kron


app = kron.create_app()
manager = Manager(app)


@manager.command
def test():
    """Run all unittests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.shell
def _make_shell_context():
    return kron.get_shell_context(app)


if __name__ == '__main__':
    manager.run()
