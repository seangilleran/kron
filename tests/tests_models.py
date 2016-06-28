import unittest

from kron import create_app, db, models


class ModelsTestCase(unittest.TestCase):

    def test_create_db_entries(self):
        archive = models.Archive.query.first()
        self.assertTrue(archive and archive.name == "Giant Bomb")

        box = models.Box.query.first()
        self.assertTrue(box and box.number == 24)

        document = models.Document.query.first()
        self.assertTrue(document and document.title == "A Letter to Brad")

        note = models.Note.query.first()
        self.assertTrue(note and note.body == "This one looks odd.")

        person = models.Person.query.first()
        self.assertTrue(person and person.name == "Ryan Davis")

        topic = models.Topic.query.first()
        self.assertTrue(topic and topic.name == "Video Games")

    def test_add_box_to_archive(self):
        box = models.Box.query.first()
        self.assertFalse(box.archive)

        archive = models.Archive.query.first()
        box.archive = archive
        db.session.add(box)
        db.session.commit()
        box_out = models.Box.query.first()
        self.assertTrue(box_out.archive and box_out.archive.id == archive.id)

    def test_add_notes_to_archive(self):
        archive = models.Archive.query.first()
        self.assertFalse(archive.notes)

        n1 = models.Note(body="Hello")
        n2 = models.Note(body="Testing")
        db.session.add_all([n1, n2])
        db.session.commit()
        self.assertTrue(n1.id and n2.id)

        archive.notes.append(n1)
        archive.notes.append(n2)
        db.session.add(archive)
        db.session.commit()
        archive_out = models.Archive.query.first()
        self.assertTrue(archive_out.notes[1].body == "Testing")

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        db.session.add_all([
            models.Archive(name="Giant Bomb"),
            models.Box(number=24),
            models.Document(title="A Letter to Brad"),
            models.Note(body="This one looks odd."),
            models.Person(name="Ryan Davis"),
            models.Topic(name="Video Games")
        ])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
