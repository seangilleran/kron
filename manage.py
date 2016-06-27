from flask_script import Manager

import kron
import kron.blog.models as blog_models


app = kron.create_app()
manager = Manager(app)


@manager.shell
def _make_shell_context():
    return dict(app=app, db=kron.db, blog_models=blog_models)


if __name__ == "__main__":
    manager.run()
