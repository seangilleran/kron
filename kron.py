from flask_script import Manager

from kron import Kron, db
from kron import Archive, Box, Document, Person, Topic, Tag, Post


app = Kron(__name__)
manager = Manager(app)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def fake_data():
    db.drop_all()
    db.create_all()

    tags = [
        Tag(name="Cool"), Tag(name="Rad"), Tag(name="Sick"), Tag(name="Dope")
    ]
    db.session.add_all(tags)
    db.session.commit()

    p1 = Post(
        title="Duis quis congue odio, efficitur fermentum libero.",
        body="Ut ligula lacus, accumsan sed libero pulvinar, lobortis " +
             "mollis diam. Sed justo neque, sagittis id mattis in, " +
             "gravida eu turpis. Suspendisse potenti. Aliquam ut tempor " +
             "augue. Ut ut urna vulputate, varius tellus id, laoreet " +
             "dui. Cras tempus tincidunt ligula ac fringilla. Curabitur " +
             "non orci ut justo euismod imperdiet sit amet eu turpis."
    )
    p1.tags.extend([tags[0], tags[1]])
    p2 = Post(
        title="Cras at massa id libero tincidunt posuere.",
        body="Ut gravida vestibulum urna, id aliquet velit luctus nec. " +
             "Aenean efficitur volutpat quam vel condimentum. Praesent " +
             "ultrices non risus non elementum. Proin a placerat felis. " +
             "Duis felis nulla, dapibus eget diam sed, euismod facilisis " +
             "lorem. Maecenas ut lacinia sapien. Nunc magna leo, vehicula " +
             "ut sagittis ac, mattis eu diam. Phasellus semper sollicitudin " +
             "augue eu auctor. Nullam rutrum congue aliquam. Proin interdum " +
             "ex non euismod accumsan. Cras dapibus egestas ipsum ac " +
             "consequat. Nam vitae ante ac sem dapibus pellentesque nec at " +
             "risus. Nam auctor massa ipsum, ut finibus arcu suscipit sed. " +
             "Pellentesque sit amet augue faucibus, imperdiet tortor eu, " +
             "hendrerit eros."
    )
    p2.tags.extend([tags[0], tags[2], tags[3]])
    db.session.add_all([p1, p2])
    db.session.commit()
    print("Done!")

    arc = Archive(name="Barkarama Karama Ding")
    db.session.add(arc)
    db.session.commit()

    t1 = Topic(name="Eternis")
    t1.citations = "Miller, 311"
    t2 = Topic(name="Chillium")
    t2.citations = "Quinn, 344"
    t2.notes = "Fugiat ad minim do duis reprehenderit pariatur aute anim."
    t3 = Topic(name="Neocent")
    t3.citations = "Burgess, 295"
    db.session.add_all([t1, t2, t3])
    db.session.commit()

    b1 = Box(number=16, archive=arc)
    b1.notes = "Veniam proident ad officia veniam ea et pariatur irure."
    b1.topics.extend([t1, t3])
    b2 = Box(number=244, archive=arc)
    b2.topics.append(t2)
    db.session.add_all([b1, b2])
    db.session.commit()

    p1 = Person(name="Wells Reilly")
    p1.citations = "Weaver, 213\r\nMiles, 117\r\nJoyner, 229"
    p1.notes = ("Ex elit ipsum ipsum magna fugiat. Laborum non non labore " +
               "incididunt. Sit tempor voluptate consequat ullamco esse.")
    p1.topics.append(t2)
    p2 = Person(name="Louisa Dudley")
    p2.citations = "Monroe, 387"
    p3 = Person(name="Carmela Buck")
    p3.citations = "Randolph, 262\r\nSullivan, 463"
    p3.topics.append(t2)
    p4 = Person(name="Dunlap Fitzpatrick")
    p4.citations = "Roberson, 456"
    p4.notes = ("Exercitation nulla ipsum minim velit ipsum velit dolore " +
               "aliqua. Ea et aliqua incididunt reprehenderit deserunt " +
               "tempor nulla duis minim laborum id quis amet ipsum. Aute " +
               "duis esse sint anim duis excepteur quis consectetur aliquip " +
               "tempor consectetur eiusmod. Consectetur adipisicing duis ad " +
               "est excepteur tempor non magna magna ut do ut elit.")
    p5 = Person(name="Hayes Fletcher")
    p5.citations = "Abbott, 396\r\nHolder, 86\r\nFaulkner, 139"
    p5.topics.extend([t1, t2, t3])
    db.session.add_all([p1, p2, p3, p4, p5])
    db.session.commit()

    d1 = Document(title="Predators And Crustaceans")
    d1.box = b1
    d1.authors.append(p1)
    d1.people.extend([p4, p5])
    d1.topics.append(t2)
    db.session.add(d1)
    db.session.commit()


@manager.shell
def _make_shell_context():
    return dict(
        app=app, db=db, Tag=Tag, Post=Post,
        Archive=Archive, Box=Box, Document=Document, Person=Person,
        Topic=Topic
    )


if __name__ == "__main__":
    manager.run()
