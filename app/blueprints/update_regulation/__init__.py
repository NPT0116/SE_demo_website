from flask import Blueprint

update_regulation_bp = Blueprint('update_regulation', __name__)

from . import routes