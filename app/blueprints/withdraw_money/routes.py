from flask import render_template, request, jsonify
from app.database import db
from datetime import datetime, timedelta
from app.regulation import regulation
from . import withdraw_money_bp

@withdraw_money_bp.route('/get_account_info', methods=['POST'])
def get_account_info():
    try:
        ma_so = request.form['ma_so']
        cursor = db.get_cursor()
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

@withdraw_money_bp.route('/get_old_balance', methods=['POST'])
def get_old_balance():
    try:
        ma_so = request.form['ma_so']
        old_balance = calculate_old_balance(ma_so)
        if old_balance:
            return jsonify({'Old balance': old_balance}), 200
        else:
            return jsonify({'message': 'Không tìm thấy thông tin tài khoản.'}), 404

    except Exception as e:
        return jsonify({'message': 'Đã xảy ra lỗi.', 'error': str(e)}), 500

@withdraw_money_bp.route('/withdraw_money')
def withdraw_money():
    return render_template('withdraw_money/withdraw_money.html')

def get_open_date(ma_so):
    cursor = db.get_cursor()
    query = "SELECT Ngay_mo FROM Tai_khoan_tiet_kiem WHERE ID_tai_khoan = %s"
    cursor.execute(query, (ma_so,))
    result = cursor.fetchone()

    if result:
        return result[0]  # Ngay_mo sẽ là phần tử đầu tiên (và duy nhất) trong kết quả
    else:
        return None  # Không tìm thấy tài khoản với mã số này
    
def validate_input(ngay_rut, ngay_mo):
    errors = []

    if ngay_rut > datetime.now().date():
        errors.append('Ngày rút không được quá ngày hiện tại.')
        
    if ngay_rut < ngay_mo:
        errors.append('Ngày rút không được trước ngày mở sổ.')
    return errors

def validate_withdraw_conditions(term, ngay_mo, ngay_giao_dich, so_tien_rut, old_balance):
    errors = []
    
    current_date = datetime.now().date()
    
    if current_date < ngay_giao_dich + timedelta(days=15):
        errors.append('Chỉ được rút sau lần giao dịch gần nhất ít nhất 15 ngày.')

    if term == 'no period':
        if int(so_tien_rut) > int(old_balance):
            errors.append('Số tiền rút không được lớn hơn số dư hiện có.')
    elif term == '3 months':
        if current_date < ngay_mo + timedelta(days=3*30):
            errors.append('Loại tiết kiệm kỳ hạn 3 tháng chỉ được rút khi quá kỳ hạn 3 tháng.')
        elif int(so_tien_rut) != int(old_balance):
            errors.append('Loại tiết kiệm kỳ hạn 3 tháng phải rút hết toàn bộ.')
    elif term == '6 months':
        if current_date < ngay_mo + timedelta(days=6*30):
            errors.append('Loại tiết kiệm kỳ hạn 6 tháng chỉ được rút khi quá kỳ hạn 6 tháng.')
        elif int(so_tien_rut) != int(old_balance):
            errors.append('Loại tiết kiệm kỳ hạn 6 tháng phải rút hết toàn bộ.')
    return errors

def validate_interest_rate(term, ngay_mo, ngay_rut):
    if term != 'no period':
        if ngay_rut >= ngay_mo + timedelta(days=3*30):
            return 0.5
        elif ngay_rut >= ngay_mo + timedelta(days=6*30):
            return 0.55
    else:
        if ngay_rut >= ngay_mo + timedelta(days=30):
            return 0.15
    return 0

def get_term(ma_so, errors):
    # Lấy loại tiết kiệm từ mã số 
    cursor = db.get_cursor()
    query = "SELECT Loai_tiet_kiem FROM Tai_khoan_tiet_kiem WHERE ID_tai_khoan = %s"
    cursor.execute(query, (ma_so,))
    result = cursor.fetchone()
    if not result:
        errors.append('Không tìm thấy thông tin tài khoản.')

    return result[0] if result else None
 
def save_data_to_database(ma_so, ngay_rut, so_tien_rut):
    cursor = db.get_cursor()

    # Tạo ID giao dịch mới
    query = "SELECT MAX(SUBSTRING(ID_giao_dich, 3)) FROM Giao_dich"
    cursor.execute(query)
    max_id = cursor.fetchone()[0]
    next_id = 1 if max_id is None else int(max_id) + 1
    new_id = f'RT{next_id:05d}'
    
    # Lưu giao dịch mới
    insert_query = """
    INSERT INTO Giao_dich (ID_giao_dich, Tai_khoan_giao_dich, Loai_giao_dich, So_tien_giao_dich, Ngay_giao_dich)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (new_id, ma_so, 'Rút Tiền', so_tien_rut, ngay_rut)
    cursor.execute(insert_query, values)
    db.connection.commit()
    
def calculate_old_balance (ma_so):
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
        old_balance = result[0] + result[1] - result[2]
    cursor.close()
    return old_balance

def calculate_nearest_transaction(ma_so):
    ngay_giao_dich = None
    cursor = db.get_cursor()
    query = """
    SELECT MAX(Ngay_giao_dich) AS ngay_giao_dich_moi_nhat
    FROM Giao_dich
    WHERE Tai_khoan_giao_dich = %s
    """

    cursor.execute(query, (ma_so,))
    result = cursor.fetchone()

    if result and result[0]:
        ngay_giao_dich = result[0]

    cursor.close()
    return ngay_giao_dich
    
@withdraw_money_bp.route('/withdraw_money/submit', methods=['POST'])
def submit_form2():
    errors = []
    try:
        ma_so = request.form['ma_so']
        khach_hang = request.form['khach_hang']
        ngay_rut = request.form['ngay_rut']
        so_tien_rut = request.form['so_tien_rut']
        ngay_rut = datetime.strptime(ngay_rut, '%Y-%m-%d').date()
        ngay_mo = get_open_date(ma_so)

        # Kiểm tra dữ liệu đầu vào
        input_errors = validate_input(ngay_rut, ngay_mo)
        if input_errors:
            return jsonify({'message': 'Đã xảy ra lỗi.', 'errors': input_errors}), 400

        # Truy vấn để lấy loại tiết kiệm từ mã số
        term_errors = []
        term = get_term(ma_so, term_errors)
        if term_errors:
            return jsonify({'message': 'Đã xảy ra lỗi.', 'errors': term_errors}), 400
      
        # Kiểm tra thỏa điều kiện rút (Đủ ngày + Số dư)
        old_balance = calculate_old_balance(ma_so)

        nearest_transaction = calculate_nearest_transaction(ma_so)
        withdraw_errors = validate_withdraw_conditions(term, ngay_mo, nearest_transaction, so_tien_rut, old_balance)
        if withdraw_errors:
            return jsonify({'message': 'Đã xảy ra lỗi.', 'errors': withdraw_errors}), 400
        
        # Tính lãi suất
        withdraw_money_after = 0
        interest_rate = validate_interest_rate(term, ngay_mo, ngay_rut)
        if interest_rate != 0:
            withdraw_money_after = int(so_tien_rut) * (1 + interest_rate)
        
        # Lưu vào database
        save_data_to_database(ma_so, ngay_rut, withdraw_money_after)
        
        return jsonify({'message': 'Dữ liệu đã được nhận và lưu thành công.'}), 200
    except Exception as e:
        return jsonify({'message': 'Đã xảy ra lỗi.', 'error': str(e)}), 500

