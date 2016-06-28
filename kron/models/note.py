from kron import db


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    html = db.Column(db.Text)
    archive_id = db.Column(db.Integer, db.ForeignKey("archives.id"))
    box_id = db.Column(db.Integer, db.ForeignKey("boxes.id"))
    citation_id = db.Column(db.Integer, db.ForeignKey("citations.id"))
    document_id = db.Column(db.Integer, db.ForeignKey("documents.id"))
    person_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    topic_id = db.Column(db.Integer, db.ForeignKey("topics.id"))

    def __repr__(self):
        return "<Note #{num}>".format(num=self.id)
