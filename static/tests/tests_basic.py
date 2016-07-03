import unittest

from kron import create_app, db


class BasicTestCase(unittest.TestCase):

    def test_app_exists(self):
        import flask
        self.assertTrue(flask.current_app)

    def test_db_exists(self):
        self.assertTrue(db)

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
