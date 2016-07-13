from flask_script import Manager

import kron.app as kron


app = kron.create_app()
manager = Manager(app)


@manager.shell
def _make_shell_context():
    return kron.get_shell_context(app)


if __name__ == '__main__':
    manager.run()

