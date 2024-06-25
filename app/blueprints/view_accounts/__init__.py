from flask import Blueprint


view_accounts_bp = Blueprint('view_accounts' , __name__)

from . import routes
