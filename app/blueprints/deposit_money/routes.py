from flask import render_template, request, jsonify
from app.database import db
from datetime import datetime
from app.regulation import regulation
from . import deposit_money_bp
from app.account import Account

def get_rate_by_id(ma_so):
    cursor = db.get_cursor()
    query = """
    SELECT
    t.ID_tai_khoan,
    t.Loai_tiet_kiem,
    r.interest_rate
    FROM
    Tai_khoan_tiet_kiem t
    JOIN
    terms r ON t.Loai_tiet_kiem = r.term_name
    WHERE
    t.ID_tai_khoan = %s;"""
    
    cursor.execute(query, (ma_so, ))
    res = cursor.fetchone()
    return res[2]

def calculate_old_balance (ma_so, interest_rate):
    old_balance = 0
    cursor = db.get_cursor()
    query = """
    SELECT 
        t.Tien_nap_ban_dau,
        IFNULL(SUM(CASE WHEN g.Loai_giao_dich = 'Nạp Tiền' THEN g.So_tien_giao_dich ELSE 0 END), 0) AS Tong_tien_nap,
        IFNULL(SUM(CASE WHEN g.Loai_giao_dich = 'Rút Tiền' THEN g.So_tien_giao_dich ELSE 0 END), 0) AS Tong_tien_rut
    FROM 
        Tai_khoan_tiet_kiem t
    LEFT JOIN 
        Giao_dich g ON t.ID_tai_khoan = g.Tai_khoan_giao_dich
    WHERE 
        t.ID_tai_khoan = %s
    GROUP BY 
        t.Tien_nap_ban_dau
    """
    cursor.execute(query, (ma_so,))
    result = cursor.fetchone()
    if result:
        old_balance = float(result[0]) + float(result[1]) - float(result[2])/(1 + interest_rate/100)

    cursor.close()
    return old_balance
    
@deposit_money_bp.route('/get_old_balance', methods=['POST'])
def get_old_balance():
    try:
        ma_so = request.form['ma_so']
        rate = get_rate_by_id(ma_so)
        old_balance = calculate_old_balance(ma_so, float(rate))
        if old_balance:
            return jsonify({'Old balance': old_balance}), 200
        else:
            return jsonify({'message': 'Không tìm thấy thông tin tài khoản.'}), 404

    except Exception as e:
        return jsonify({'message': 'Đã xảy ra lỗi.', 'error': str(e)}), 500

@deposit_money_bp.route('/get_account_info', methods=['POST'])
def get_account_info():
    try:
        ma_so = request.form['ma_so']
        cursor = db.get_cursor()
        account = Account(ma_so)
        query = """
            SELECT k.Ho_ten 
            FROM Tai_khoan_tiet_kiem t
            JOIN Khach_hang k ON t.Nguoi_so_huu = k.Chung_minh_Thu
            WHERE t.ID_tai_khoan = %s
        """
        cursor.execute(query, (ma_so,))
        result = cursor.fetchone()
        
        if result:
            return jsonify({'ten_tai_khoan': result[0]}), 200
        else:
            return jsonify({'message': 'Không tìm thấy thông tin tài khoản.'}), 404

    except Exception as e:
        return jsonify({'message': 'Đã xảy ra lỗi.', 'error': str(e)}), 500

@deposit_money_bp.route('/deposit_money')
def deposit_money():
    return render_template('deposit_money/deposit_money.html')

def get_open_date(ma_so):
    cursor = db.get_cursor()
    query = "SELECT Ngay_mo FROM Tai_khoan_tiet_kiem WHERE ID_tai_khoan = %s"
    cursor.execute(query, (ma_so,))
    result = cursor.fetchone()

    if result:
        return result[0]  # Ngay_mo sẽ là phần tử đầu tiên (và duy nhất) trong kết quả
    else:
        return None  # Không tìm thấy tài khoản với mã số này
    
def validate_input(ma_so, khach_hang, so_tien_gui, ngay_gui):
    errors = []
    
    # Kiểm tra dữ liệu đầu vào 
    if any(char.isdigit() for char in khach_hang):
        errors.append('Tên khách hàng không được chứa số.')
    
    if any(char.isalpha() for char in so_tien_gui):
        errors.append('Số tiền gửi không được chứa chữ.')

    if ngay_gui > datetime.now().date():
        errors.append('Ngày gửi không được quá ngày hiện tại.')
        
    if ngay_gui < get_open_date(ma_so):
        errors.append('Ngày gửi không được trước ngày mở sổ.')
    return errors
        
def get_term(ma_so, errors):
    # Lấy loại tiết kiệm từ mã số 
    cursor = db.get_cursor()
    query = "SELECT Loai_tiet_kiem FROM Tai_khoan_tiet_kiem WHERE ID_tai_khoan = %s"
    cursor.execute(query, (ma_so,))
    result = cursor.fetchone()
    if not result:
        errors.append('Không tìm thấy thông tin tài khoản.')

    return result[0] if result else None
 
def validate_deposit_conditions(so_tien_gui, loai_tiet_kiem):
    errors = []
    # Kiểm tra điều kiện gửi tiền 
    if loai_tiet_kiem != 'no period':
        err = 'Chỉ nhận gửi tiền cho loại tiết kiệm "no period". ' + 'Loại tiết kiệm của sổ là ' + loai_tiet_kiem 
        errors.append(err)

    minimum_deposit_amount = regulation.get_minimum_deposit_money()
    
    if int(so_tien_gui) < minimum_deposit_amount:
        errors.append(f'Số tiền gửi tối thiểu là {minimum_deposit_amount} VND.')
    return errors
        
def save_data_to_database(ma_so, ngay_gui, so_tien_gui):
    cursor = db.get_cursor()

    # Tạo ID giao dịch mới
    query = "SELECT MAX(SUBSTRING(ID_giao_dich, 3)) FROM Giao_dich"
    cursor.execute(query)
    max_id = cursor.fetchone()[0]
    next_id = 1 if max_id is None else int(max_id) + 1
    new_id = f'NT{next_id:05d}'
    
    # Lưu giao dịch mới
    insert_query = """
    INSERT INTO Giao_dich (ID_giao_dich, Tai_khoan_giao_dich, Loai_giao_dich, So_tien_giao_dich, Ngay_giao_dich)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (new_id, ma_so, 'Nạp Tiền', so_tien_gui, ngay_gui)
    cursor.execute(insert_query, values)
    db.connection.commit()

def account_status(ma_so):
    cursor = db.get_cursor()
    query = """
    SELECT Trang_thai_tai_khoan
    FROM Tai_khoan_tiet_kiem
    WHERE ID_tai_khoan = %s
    """
    cursor.execute(query, (ma_so, ))
    res = cursor.fetchone()
    return res[0]

@deposit_money_bp.route('/deposit_money/submit', methods=['POST'])
def submit_form2():
    try:
        # Xử lý dữ liệu nhận được từ form
        ma_so = request.form['ma_so']
        khach_hang = request.form['khach_hang']
        ngay_gui = request.form['ngay_goi']
        so_tien_gui = request.form['so_tien_gui']
        ngay_gui = datetime.strptime(ngay_gui, '%Y-%m-%d').date()
        
        # Kiểm tra sổ đóng 
        status = []
        if int(account_status(ma_so)) == 0:
            status.append('Sổ đã đóng')
            return jsonify({'message': 'Đã xảy ra lỗi.', 'errors': status}), 400
        
        # Kiểm tra dữ liệu đầu vào
        input_errors = validate_input(ma_so, khach_hang, so_tien_gui, ngay_gui)
        if input_errors:
            return jsonify({'message': 'Đã xảy ra lỗi.', 'errors': input_errors}), 400
        
        # Truy vấn để lấy loại tiết kiệm từ mã số
        term_errors = []
        loai_tiet_kiem = get_term(ma_so, term_errors)

        if term_errors:
            return jsonify({'message': 'Đã xảy ra lỗi.', 'errors': term_errors}), 400

        # Kiểm tra điều kiện gửi tiền
        deposit_errors = validate_deposit_conditions(so_tien_gui, loai_tiet_kiem)
        if deposit_errors:
            return jsonify({'message': 'Đã xảy ra lỗi.', 'errors': deposit_errors}), 400
        
        # Lưu dữ liệu vào cơ sở dữ liệu
        save_data_to_database(ma_so, ngay_gui, so_tien_gui)

        return jsonify({'message': 'Dữ liệu đã được nhận và lưu thành công.'}), 200
    except Exception as e:
        return jsonify({'message': 'Đã xảy ra lỗi.', 'error': str(e)}), 500
