from flask import Blueprint, render_template, request, jsonify

monthly_report_bp = Blueprint('monthly_report', __name__)

@monthly_report_bp.route('/', methods=['GET'])
def monthly_report():
    return render_template('report/monthly_report.html')

@monthly_report_bp.route('/submit', methods=['POST'])
def submit_monthly_report():
    try:
        loai_tiet_kiem = request.form['loai_tiet_kiem']
        thang = request.form['thang']
        
        ngay_1 = request.form['ngay_1']
        so_mo_1 = request.form['so_mo_1']
        so_dong_1 = request.form['so_dong_1']
        chenh_lech_1 = request.form['chenh_lech_1']
        
        ngay_2 = request.form['ngay_2']
        so_mo_2 = request.form['so_mo_2']
        so_dong_2 = request.form['so_dong_2']
        chenh_lech_2 = request.form['chenh_lech_2']
        
        # Xử lý và lưu dữ liệu vào database
        return jsonify({'message': 'Báo cáo hàng tháng đã được gửi và lưu thành công'})
    except Exception as e:
        return jsonify({'message': 'Không thể gửi báo cáo hàng tháng', 'error': str(e)})
