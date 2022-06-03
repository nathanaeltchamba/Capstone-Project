from flask import Blueprint

bp = Blueprint('users',__name__, template_folder='users', url_prefix='user')

from .import routes, models