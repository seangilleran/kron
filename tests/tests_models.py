import unittest

from kron import create_app, db, models


class ModelsTestCase(unittest.TestCase):

    def test_create_db_entries(self):
        self.assertTrue(
            models.Archive.query.first() and
            models.Box.query.first() and
            models.Document.query.first() and
            models.Person.query.first() and
            models.Topic.query.first()
        )

    def test_add_box_to_archive(self):
        a = models.Archive.query.first()
        b = models.Box(number=15)
        a.boxes.append(b)
        self.assertTrue(a.boxes[0] == b and b.archive == a)

    def test_add_archive_to_box(self):
        b = models.Box.query.first()
        a = models.Archive(name="Test")
        b.archive = a
        self.assertTrue(b.archive == a and a.boxes[0] == b)

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        db.session.add_all([
            models.Archive(name="Giant Bomb"),
            models.Box(number=24),
            models.Document(title="A Letter to Brad"),
            models.Person(name="Ryan Davis"),
            models.Topic(name="Video Games")
        ])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
