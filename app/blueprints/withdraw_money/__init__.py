from flask import Blueprint

withdraw_money_bp = Blueprint('withdraw_money', __name__)

from . import routes