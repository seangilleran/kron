from time import time
from math import floor

from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment


db = SQLAlchemy()
moment = Moment()


def uniqid():
    t = time()
    return "%05x" %int((t-floor(t))*1000000)
