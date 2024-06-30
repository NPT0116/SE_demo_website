from flask import Blueprint

report_bp = Blueprint('report', __name__, template_folder="templates/report" )

from .daily_report import daily_report_bp
from .monthly_report import monthly_report_bp
from . import routes
# Đăng ký các Blueprints con
report_bp.register_blueprint(daily_report_bp, url_prefix='/daily')
report_bp.register_blueprint(monthly_report_bp, url_prefix='/monthly')
