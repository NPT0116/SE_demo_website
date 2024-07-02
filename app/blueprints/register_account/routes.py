from flask import render_template, request, jsonify
from datetime import datetime
from app.database import db
from . import register_account_bp
from app.regulation import regulation
 # Gọi phương thức để lấy giá trị
terms = []
minimum_deposit_money = int()

@register_account_bp.route('/register_account')
def register_account():
    t = regulation.get_terms()  # Gọi phương thức để lấy giá trị
    minimum_deposit_money = regulation.get_minimum_deposit_money() 
    print ("period: ", terms)
    print ("minimum deposit: ", minimum_deposit_money )
    return render_template('register_account.html')

@register_account_bp.route('/register_account/submit', methods=['POST'])
def submit_register_account():
    errors = []
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
        
        # Kiểm tra các điều kiện
        if any(char.isdigit() for char in khach_hang):
            errors.append('Tên khách hàng không được chứa số.')

        if any(char.isalpha() for char in cmnd):
            errors.append('Số CMND không được chứa chữ.')

        if any(char.isalpha() for char in so_tien_gui):
            errors.append('Số tiền gửi không được chứa chữ.')

        if loai_tiet_kiem not in regulation.get_terms():
            errors.append('Loại kỳ hạn tiết kiệm không hợp lệ.')

        if int(so_tien_gui) < regulation.get_minimum_deposit_money():
            errors.append(f'Số tiền gửi tối thiểu là {regulation.get_minimum_deposit_money()} VND.')
            
        if ngay_mo_so > datetime.now().date():
            errors.append('Ngày mở sổ không được quá ngày hiện tại.')

        # Nếu có lỗi, trả về phản hồi với danh sách lỗi
        if errors:
            return jsonify({'message': 'Có lỗi xảy ra.', 'errors': errors}), 400

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
        return jsonify({'message': 'Đã xảy ra lỗi.', 'error': str(e)}), 500
