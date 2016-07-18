import unittest

import forgery_py

import kron
from kron import db
from kron.models import Archive, Box, Document, Tag, TagType


class ModelsTestCase(unittest.TestCase):
    """Test data models."""

    def test_archive(self):
        a = Archive(forgery_py.lorem_ipsum.title())
        a.save()
        self.assertTrue(a in Archive.query.all())
        self.assertTrue(a.id and a.id_hash)

        t = Tag(forgery_py.lorem_ipsum.title())
        t.save()
        a.tags.append(t)
        a.save()
        self.assertTrue(t in a.tags and a in t.archives)
        t.archives.remove(a)
        t.save()
        self.assertFalse(t in a.tags and a in t.archives)

        a.delete()
        self.assertFalse(a in Archive.query.all())

        lastid = ''
        match = False
        l = []
        for _ in range(1000):
            l.append(Archive(forgery_py.lorem_ipsum.title()))
        db.session.add_all(l)
        db.session.commit()
        for a in Archive.query.all():
            if a.id_hash == lastid:
                match = True
                break
            lastid = a.id_hash
        self.assertFalse(match)

    def test_box(self):
        b = Box(forgery_py.lorem_ipsum.title())
        b.save()
        self.assertTrue(b in Box.query.all())
        self.assertTrue(b.id and b.id_hash)

        t = Tag(forgery_py.lorem_ipsum.title())
        t.save()
        b.tags.append(t)
        b.save()
        self.assertTrue(t in b.tags and b in t.boxes)
        t.boxes.remove(b)
        t.save()
        self.assertFalse(t in b.tags and b in t.boxes)

        b.delete()
        self.assertFalse(b in Box.query.all())

        lastid = ''
        match = False
        l = []
        for _ in range(1000):
            l.append(Box(forgery_py.lorem_ipsum.title()))
        db.session.add_all(l)
        db.session.commit()
        for b in Box.query.all():
            if b.id_hash == lastid:
                match = True
                break
            lastid = b.id_hash
        self.assertFalse(match)

    def test_document(self):
        d = Document(forgery_py.lorem_ipsum.title())
        d.save()
        self.assertTrue(d in Document.query.all())
        self.assertTrue(d.id and d.id_hash)

        t = Tag(forgery_py.lorem_ipsum.title())
        t.save()
        d.tags.append(t)
        d.save()
        self.assertTrue(t in d.tags and d in t.documents)
        t.documents.remove(d)
        t.save()
        self.assertFalse(t in d.tags and d in t.documents)

        d.delete()
        self.assertFalse(d in Document.query.all())

        lastid = ''
        match = False
        l = []
        for _ in range(1000):
            l.append(Document(forgery_py.lorem_ipsum.title()))
        db.session.add_all(l)
        db.session.commit()
        for d in Document.query.all():
            if d.id_hash == lastid:
                match = True
                break
            lastid = d.id_hash
        self.assertFalse(match)

    def test_tag(self):
        t = Tag(forgery_py.lorem_ipsum.title())
        t.save()
        self.assertTrue(t in Tag.query.all())
        self.assertTrue(t.id and t.id_hash)

        t1 = Tag(forgery_py.lorem_ipsum.title())
        t1.save
        t.tags.append(t1)
        t.save()
        self.assertTrue(t in t1.refs and t1 in t.tags)
        t1.refs.remove(t)
        t1.save()
        self.assertFalse(t in t1.refs and t1 in t.tags)

        t.delete()
        self.assertFalse(t in Tag.query.all())

        lastid = ''
        match = False
        l = []
        for _ in range(100):
            l.append(Tag(forgery_py.lorem_ipsum.title()))
        db.session.add_all(l)
        db.session.commit()
        for t in Tag.query.all():
            if t.id_hash == lastid:
                match = True
                break
            lastid = t.id_hash
        self.assertFalse(match)

    def test_tagtype(self):
        tt = TagType(forgery_py.lorem_ipsum.title())
        tt.save()
        self.assertTrue(tt in TagType.query.all())
        self.assertTrue(tt.id and tt.id_hash)
        tt.delete()
        self.assertFalse(tt in TagType.query.all())

        lastid = ''
        match = False
        l = []
        for _ in range(100):
            l.append(TagType(forgery_py.lorem_ipsum.title()))
        db.session.add_all(l)
        db.session.commit()
        for tt in TagType.query.all():
            if tt.id_hash == lastid:
                match = True
                break
            lastid = tt.id_hash
        self.assertFalse(match)

    def test_archive_boxes(self):
        a = Archive(forgery_py.lorem_ipsum.title())
        b = Box(forgery_py.lorem_ipsum.title())
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
        b = Box(forgery_py.lorem_ipsum.title())
        d = Document(forgery_py.lorem_ipsum.title())
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
        t = Tag(forgery_py.lorem_ipsum.title())
        tt = TagType(forgery_py.lorem_ipsum.title())
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
