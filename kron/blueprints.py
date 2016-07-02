from flask import Blueprint

api = Blueprint("api", __name__)

from kron.api import *
