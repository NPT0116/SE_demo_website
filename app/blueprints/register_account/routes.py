from flask import render_template, request, jsonify
from datetime import datetime
from app.database import db
from . import register_account_bp
from app.regulation import regulation

@register_account_bp.route('/register_account')
def register_account():
    t = regulation.get_terms()  # Gọi phương thức để lấy giá trị
    minimum_deposit_money = regulation.get_minimum_deposit_money()
    print("period: ", t)
    print("minimum deposit: ", minimum_deposit_money)
    return render_template('register_account/register_account.html')

def validate_input(khach_hang, cmnd, so_tien_gui, loai_tiet_kiem, ngay_mo_so):
    errors = []
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
    return errors

def check_and_add_customer(cmnd, khach_hang, dia_chi):
    cursor = db.get_cursor()
    check_customer_query = "SELECT Ho_ten, Dia_chi FROM Khach_hang WHERE Chung_minh_Thu = %s"
    cursor.execute(check_customer_query, (cmnd,))
    result = cursor.fetchone()

    errors = []

    if result:
        existing_name, existing_address = result
        if khach_hang != existing_name:
            error_name = 'Họ tên khách hàng không khớp với dữ liệu hiện tại: ' + existing_name
            errors.append(error_name)
        if dia_chi != existing_address:
            error_address = 'Địa chỉ khách hàng không khớp với dữ liệu hiện tại: ' + existing_address
            errors.append(error_address)
    else:
        insert_customer_query = """
        INSERT INTO Khach_hang (Ho_ten, Chung_minh_Thu, Dia_chi)
        VALUES (%s, %s, %s)
        """
        cursor.execute(insert_customer_query, (khach_hang, cmnd, dia_chi))
        db.connection.commit()
    return errors

def get_next_account_id():
    cursor = db.get_cursor()

    # Tìm mã số tài khoản lớn nhất hiện có
    max_id_query = "SELECT MAX(CAST(SUBSTRING(ID_tai_khoan, 4) AS UNSIGNED)) FROM Tai_khoan_tiet_kiem"
    cursor.execute(max_id_query)
    max_id = cursor.fetchone()[0]
    
    if not max_id:
        # Nếu không có bản ghi nào trong bảng
        return 'STK00001'

    # Tạo một danh sách các mã số tài khoản hiện có
    all_ids_query = "SELECT CAST(SUBSTRING(ID_tai_khoan, 4) AS UNSIGNED) FROM Tai_khoan_tiet_kiem ORDER BY ID_tai_khoan"
    cursor.execute(all_ids_query)
    existing_ids = [row[0] for row in cursor.fetchall()]

    # Tìm lỗ trống trong dãy số
    for i in range(1, max_id + 1):
        if i not in existing_ids:
            return f'STK{i:05d}'

    # Nếu không có lỗ trống, sử dụng mã số tài khoản lớn nhất + 1
    return f'STK{max_id + 1:05d}'

@register_account_bp.route('/register_account/submit', methods=['POST'])
def submit_register_account():
    errors = []
    try:
        loai_tiet_kiem = request.form['loai_tiet_kiem']
        khach_hang = request.form['khach_hang']
        cmnd = request.form['cmnd']
        dia_chi = request.form['dia_chi']
        ngay_mo_so = request.form['ngay_mo_so']
        so_tien_gui = request.form['so_tien_gui']
        ngay_mo_so = datetime.strptime(ngay_mo_so, '%Y-%m-%d').date()

        errors = validate_input(khach_hang, cmnd, so_tien_gui, loai_tiet_kiem, ngay_mo_so)
        if errors:
            return jsonify({'message': 'Đã xảy ra lỗi.', 'errors': errors}), 400
        
        customer_error = check_and_add_customer(cmnd, khach_hang, dia_chi)
        if customer_error:
            return jsonify({'message': 'Đã xảy ra lỗi.', 'errors': customer_error}), 400
        
        ma_so = get_next_account_id()
        
        insert_account_query = """
        INSERT INTO Tai_khoan_tiet_kiem (ID_tai_khoan, Ngay_mo, Nguoi_so_huu, Loai_tiet_kiem, Tien_nap_ban_dau, Lai_suat)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        rate = regulation.get_interest_rate(loai_tiet_kiem)
        so_tien_gui = float(so_tien_gui)
        values = (ma_so, ngay_mo_so, cmnd, loai_tiet_kiem, so_tien_gui, rate)

        cursor = db.get_cursor()
        cursor.execute(insert_account_query, values)
        db.connection.commit()

        return jsonify({'message': 'Dữ liệu đã được gửi và lưu thành công'})
    except Exception as e:
        return jsonify({'message': 'Đã xảy ra lỗi.', 'error': str(e)}), 500
