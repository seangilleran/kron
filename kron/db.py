from datetime import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment


db = SQLAlchemy()
moment = Moment()


def is_ok(data):
    if not data or data == "" or data == [] or data == {} or data == [{}]:
        return False
    return True


class ModelEventListeners():
    @staticmethod
    def on_update(target, value, oldvalue, initiator):
        target.last_update = datetime.utcnow()
