from flask import Blueprint

deposit_money_bp = Blueprint('deposit_money', __name__, template_folder="../../templates")

from . import routes
