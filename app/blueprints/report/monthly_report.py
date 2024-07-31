from flask import Blueprint, render_template, request, jsonify
from app.database import db
from app.regulation import regulation  # Ensure this is the correct import path

monthly_report_bp = Blueprint('monthly_report', __name__)

@monthly_report_bp.route('/', methods=['GET'])
def monthly_report():
<<<<<<< HEAD
    terms = regulation.get_terms()  # Fetch the terms for the dropdown
    return render_template('report/monthly_report.html', terms=terms)
=======
    return render_template('report/monthly_report.html')
@monthly_report_bp.route('/chart', methods=['GET'])
def monthly_chart_report():
    return render_template('report/monthly_chart.html')
>>>>>>> e86d4c31555f0721e13bd4136ae48187f0a73f79

@monthly_report_bp.route('/submit', methods=['POST'])
def submit_monthly_report():
    try:
        print(request.form)
        loai_tiet_kiem = request.form['term']
        thang = int(request.form['selected_month']) + 1
        nam = int(request.form['year'])
        formatted = str(nam) + "-" + str(thang).zfill(2)
        print(formatted)
        query = f"call ngay_mo_so_dong_so('{formatted}', N'{loai_tiet_kiem}')"
        print(query)
        cursor = db.get_cursor()
        cursor.execute(query)
        monthly_reports = cursor.fetchall()
        print(monthly_reports)
        return render_template('report/monthly_report.html', reports=monthly_reports)
    except Exception as e:
        return jsonify({'message': 'Không thể gửi báo cáo hàng tháng', 'error': str(e)})


@monthly_report_bp.route('/get_info', methods=['POST'])
def get_monthly_chart():
    try:
        data = request.json
        loai_tiet_kiem = data['loai_tiet_kiem']
        thang = data['thang']
        query = f"call ngay_mo_so_dong_so('{thang}', N'{loai_tiet_kiem}')"
        cursor = db.get_cursor()
        cursor.execute(query)
        monthly_reports = cursor.fetchall()
        result = [
            {
                "ngay": row[0].day,
                "mo_so": row[1],
                "dong_so": row[2]
            }
            for row in monthly_reports
        ]
        print (result)
        return jsonify(result)
    except Exception as e:
        return jsonify({'message': 'Không thể gửi báo cáo hàng tháng', 'error': str(e)}), 500