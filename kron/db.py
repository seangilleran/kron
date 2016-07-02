from time import time
from math import floor

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def uniqid():
    t = time()
    return "%05x" %int((t-floor(t))*1000000)
