import flask


#
# Time helpers
#

def utcnow():
    """Find current utc time."""

    from datetime import datetime
    import pytz

    return datetime.now(tz=pytz.utc)


def isostrptime(timestr):
    """Convert iso time string into datetime."""

    from datetime import datetime
    import re

    t = re.sub(r'[:]|([-](?!((\d{2}[:]\d{2})|(\d{4}))$))', '', timestr)
    return datetime.strptime(t, '%Y%m%dT%H%M%S.%f%z')


#
# Model helpers
#

def create_id_hash(model, obj):
    """Create a unique id hash to obscure the actual row #."""

    from flask import current_app as app
    from hashids import Hashids

    base = model.__tableid__ + obj.id
    hid = Hashids(app.config['SECRET_KEY'], 8)
    return hid.encode(base)


def update_event(model, connection, target):
    """Base update/insert listener for models."""

    values = dict(last_modified=utcnow().isoformat())
    if not target.id_hash:
        values['id_hash'] = create_id_hash(model, target)

    t = model.__table__
    if not target.id_hash:
        connection.execute(
            t.update().
                where(t.c.id==target.id).
                values(values)
        )


#
# View helpers
#

def find_or_404(obj, id):
    """Find an object instance by id_hash."""

    rv = obj.query.filter_by(id_hash=id).first()
    if not rv:
        flask.abort(404)
    return rv


def get_json_payload(req, keys=['name']):
    """Retrieve the JSON payload from a flask.request."""

    rv = req.get_json()
    if not rv:
        flask.abort(415)
    for key in keys:
        if key not in rv:
            flask.abort(415)
    return rv


def use_cached(obj, headers):
    """Use request headers to check if client's copy is outdated."""

    if headers.get('If-Modified-Since'):
        c_timestamp = isostrptime(headers['If-Modified-Since'])
        l_timestamp = isostrptime(obj.last_modified)
        if c_timestamp >= l_timestamp:
            return True
    return False


def make_res(payload, headers=None, code=200, jsonify=False):
    if jsonify:
        payload = flask.jsonify(payload)
    rv = flask.make_response(payload, code)
    if headers:
        for h in headers:
            rv.headers[h] = headers[h]
    return rv


def redirect(uri):
    """Return headers for permanent redirect."""

    res = flask.make_response(flask.redirect(uri, code=301))
    res.headers['Location'] = uri
    return res
