from flask import Blueprint, render_template, request, jsonify

daily_report_bp = Blueprint('daily_report', __name__)

@daily_report_bp.route('/', methods=['GET'])
def daily_report():
    return render_template('report/daily_report.html')

@daily_report_bp.route('/submit', methods=['POST'])
def submit_daily_report():
    try:
        ngay = request.form['ngay']

        
        # Xử lý và lưu dữ liệu vào database
        return jsonify({'message': 'Báo cáo hàng ngày đã được gửi và lưu thành công'})
    except Exception as e:
        return jsonify({'message': 'Không thể gửi báo cáo hàng ngày', 'error': str(e)})
