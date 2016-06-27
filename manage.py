import os
import uuid

from flask_script import Manager

from kron.app import create_app
import kron.models as models
import kron.blog.models as blog_models
import kron.blog.blueprints as blog_blueprints


app = create_app(models.db, [blog_blueprints.blog])
manager = Manager(app)


@manager.shell
def _make_shell_context():
    return dict(app=app, db=models.db, models=models,
                blog_models=blog_models)


if __name__ == "__main__":
    manager.run()
