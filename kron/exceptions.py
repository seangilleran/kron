from flask import jsonify


class APIInvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        if status_code:
            self.status_code = status_code
        self.message = message
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


class APINotFound(Exception):
    status_code = 404
    message = "Requested resource could not be found."

    def __init__(self, message=None, payload=None):
        Exception.__init__(self)
        if message:
            self.message = message
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv
