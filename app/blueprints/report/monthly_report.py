from flask import Blueprint, render_template, request, jsonify
from app.database import db


monthly_report_bp = Blueprint('monthly_report', __name__)

@monthly_report_bp.route('/', methods=['GET'])
def monthly_report():
    return render_template('report/monthly_report.html')

@monthly_report_bp.route('/submit', methods=['POST'])
def submit_monthly_report():
    try:
        loai_tiet_kiem = request.form['loai_tiet_kiem']
        thang = request.form['thang']
        query = f"call ngay_mo_so_dong_so('{thang}', N'{loai_tiet_kiem}')"
        print(query)
        cursor = db.get_cursor()
        cursor.execute(query)
        monthly_reports = cursor.fetchall()
        return render_template('report/monthly_report.html', reports = monthly_reports)
    except Exception as e:
        return jsonify({'message': 'Không thể gửi báo cáo hàng tháng', 'error': str(e)})
