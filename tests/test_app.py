import unittest

from flask import current_app as app

import kron


class AppTestCase(unittest.TestCase):
    """Test app factory."""

    def test_app_exists(self):
        self.assertTrue(app)

    def setUp(self):
        self.app = kron.create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
