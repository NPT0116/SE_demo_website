from flask import Blueprint

register_account_bp = Blueprint('register_account', __name__, template_folder="/register_account", static_folder="static/home")

from . import routes
