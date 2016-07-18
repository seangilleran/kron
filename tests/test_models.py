import unittest

import forgery_py

import kron
from kron import db
import kron.models as models


class ModelsTestCase(unittest.TestCase):
    """Test data models."""

    def test_archive(self):
        a = models.Archive(forgery_py.lorem_ipsum.title())
        a.save()
        self.assertTrue(a in models.Archive.query.all())
        self.assertTrue(a.id and a.id_hash)
        a.delete()
        self.assertFalse(a in models.Archive.query.all())

        lastid = ''
        match = False
        l = []
        for _ in range(1000):
            l.append(models.Archive(forgery_py.lorem_ipsum.title()))
        db.session.add_all(l)
        db.session.commit()
        for a in models.Archive.query.all():
            if a.id_hash == lastid:
                match = True
                break
            lastid = a.id_hash
        self.assertFalse(match)

    def test_box(self):
        b = models.Box(forgery_py.lorem_ipsum.title())
        b.save()
        self.assertTrue(b in models.Box.query.all())
        self.assertTrue(b.id and b.id_hash)
        b.delete()
        self.assertFalse(b in models.Box.query.all())

        lastid = ''
        match = False
        l = []
        for _ in range(1000):
            l.append(models.Box(forgery_py.lorem_ipsum.title()))
        db.session.add_all(l)
        db.session.commit()
        for b in models.Box.query.all():
            if b.id_hash == lastid:
                match = True
                break
            lastid = b.id_hash
        self.assertFalse(match)

    def test_document(self):
        d = models.Document(forgery_py.lorem_ipsum.title())
        d.save()
        self.assertTrue(d in models.Document.query.all())
        self.assertTrue(d.id and d.id_hash)
        d.delete()
        self.assertFalse(d in models.Document.query.all())

        lastid = ''
        match = False
        l = []
        for _ in range(1000):
            l.append(models.Document(forgery_py.lorem_ipsum.title()))
        db.session.add_all(l)
        db.session.commit()
        for d in models.Document.query.all():
            if d.id_hash == lastid:
                match = True
                break
            lastid = d.id_hash
        self.assertFalse(match)

    def test_tag(self):
        t = models.Tag(forgery_py.lorem_ipsum.title())
        t.save()
        self.assertTrue(t in models.Tag.query.all())
        self.assertTrue(t.id and t.id_hash)
        t.delete()
        self.assertFalse(t in models.Tag.query.all())

        lastid = ''
        match = False
        l = []
        for _ in range(100):
            l.append(models.Tag(forgery_py.lorem_ipsum.title()))
        db.session.add_all(l)
        db.session.commit()
        for t in models.Tag.query.all():
            if t.id_hash == lastid:
                match = True
                break
            lastid = t.id_hash
        self.assertFalse(match)

    def test_tagtype(self):
        tt = models.TagType(forgery_py.lorem_ipsum.title())
        tt.save()
        self.assertTrue(tt in models.TagType.query.all())
        self.assertTrue(tt.id and tt.id_hash)
        tt.delete()
        self.assertFalse(tt in models.TagType.query.all())

        lastid = ''
        match = False
        l = []
        for _ in range(100):
            l.append(models.TagType(forgery_py.lorem_ipsum.title()))
        db.session.add_all(l)
        db.session.commit()
        for tt in models.TagType.query.all():
            if tt.id_hash == lastid:
                match = True
                break
            lastid = tt.id_hash
        self.assertFalse(match)

    def test_archive_boxes(self):
        a = models.Archive(forgery_py.lorem_ipsum.title())
        b = models.Box(forgery_py.lorem_ipsum.title())
        db.session.add_all([a, b])
        db.session.commit()
        a.boxes.append(b)
        a.save
        self.assertTrue(b in a.boxes and b.archive == a)
        b.archive = None
        b.save()
        self.assertFalse(b in a.boxes and b.archive == a)
        self.assertFalse(a.boxes.first())
        self.assertFalse(b.archive)

    def test_box_documents(self):
        b = models.Box(forgery_py.lorem_ipsum.title())
        d = models.Document(forgery_py.lorem_ipsum.title())
        db.session.add_all([b, d])
        db.session.commit()
        d.box = b
        d.save()
        self.assertTrue(d.box == b and d in b.documents)
        b.documents.remove(d)
        b.save()
        self.assertFalse(d.box == b and d in b.documents)
        self.assertFalse(d.box)
        self.assertFalse(b.documents.first())

    def test_tag_tagtypes(self):
        t = models.Tag(forgery_py.lorem_ipsum.title())
        tt = models.TagType(forgery_py.lorem_ipsum.title())
        db.session.add_all([t, tt])
        db.session.commit()
        t.tagtype = tt
        t.save()
        self.assertTrue(t.tagtype == tt and t in tt.tags)
        tt.tags.remove(t)
        tt.save()
        self.assertFalse(t.tagtype == tt and t in tt.tags)
        self.assertFalse(t.tagtype)
        self.assertFalse(tt.tags.first())

    def setUp(self):
        self.app = kron.create_app(testing=True)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
