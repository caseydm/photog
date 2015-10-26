from flask import Blueprint

accounts = Blueprint('accounts', __name__)

from . import views
