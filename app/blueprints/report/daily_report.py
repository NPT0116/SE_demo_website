from flask import Blueprint, render_template, request, jsonify

daily_report_bp = Blueprint('daily_report', __name__)

@daily_report_bp.route('/', methods=['GET'])
def daily_report():
    return render_template('daily_report.html')

@daily_report_bp.route('/submit', methods=['POST'])
def submit_daily_report():
    try:
        ngay = request.form['ngay']
        loai_tiet_kiem_1 = request.form['loai_tiet_kiem_1']
        tong_thu_1 = request.form['tong_thu_1']
        tong_chi_1 = request.form['tong_chi_1']
        chenh_lech_1 = request.form['chenh_lech_1']
        
        loai_tiet_kiem_2 = request.form['loai_tiet_kiem_2']
        tong_thu_2 = request.form['tong_thu_2']
        tong_chi_2 = request.form['tong_chi_2']
        chenh_lech_2 = request.form['chenh_lech_2']
        
        # Xử lý và lưu dữ liệu vào database
        return jsonify({'message': 'Báo cáo hàng ngày đã được gửi và lưu thành công'})
    except Exception as e:
        return jsonify({'message': 'Không thể gửi báo cáo hàng ngày', 'error': str(e)})
