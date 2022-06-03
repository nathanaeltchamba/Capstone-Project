from flask import Blueprint

bp = Blueprint('shop', __name__, template_folder='shop', url_prefix='shop')

from .import routes, models