from flask import render_template, request, jsonify
from datetime import datetime
from app.database import db
from . import register_account_bp

@register_account_bp.route('/register_account')
def register_account():
    return render_template('register_account.html')

@register_account_bp.route('/submit_register_account', methods=['POST'])
def submit_register_account():
    try:
        # Xử lý dữ liệu nhận được từ form
        ma_so = request.form['ma_so']
        loai_tiet_kiem = request.form['loai_tiet_kiem']

        khach_hang = request.form['khach_hang']
        cmnd = request.form['cmnd']
        dia_chi = request.form['dia_chi']
        ngay_mo_so = request.form['ngay_mo_so']
        so_tien_gui = request.form['so_tien_gui']
        ngay_mo_so = datetime.strptime(ngay_mo_so, '%Y-%m-%d').date()

        # Truy vấn để chèn dữ liệu vào bảng
        query = """
        INSERT INTO create_account (ma_so, loai_tiet_kiem, khach_hang, cmnd, dia_chi, ngay_mo_so, so_tien_gui)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (ma_so, loai_tiet_kiem, khach_hang, cmnd, dia_chi, ngay_mo_so, so_tien_gui)
        
        cursor = db.get_cursor()
        cursor.execute(query, values)
        db.connection.commit()  # Đảm bảo rằng giao dịch được ghi vào cơ sở dữ liệu
        return jsonify({'message': 'Dữ liệu đã được gửi và lưu thành công'})
    except Exception as e:
        return jsonify({'message': 'khong co loai ky han do', 'error': str(e)})
