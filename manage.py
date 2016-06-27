from flask_script import Manager

import kron
import kron.models as models


app = kron.create_app()
manager = Manager(app)


@manager.shell
def _make_shell_context():
    return dict(app=app, db=kron.db, models=models)


if __name__ == "__main__":
    manager.run()
