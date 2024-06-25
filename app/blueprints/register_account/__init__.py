from flask import Blueprint

register_account_bp = Blueprint('register_account', __name__)

from . import routes
