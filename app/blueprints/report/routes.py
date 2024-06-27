from flask import render_template, request, jsonify
from app.database import db
from . import report_bp
 # Gọi phương thức để lấy giá trị


@report_bp.route('/')
def register_account():
    return render_template('report.html')