from flask import Blueprint

form2_bp = Blueprint('deposit_money', __name__)

from . import routes
