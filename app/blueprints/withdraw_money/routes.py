from flask import render_template, request, jsonify
from app.database import db
from datetime import datetime, timedelta
from app.regulation import regulation
from . import withdraw_money_bp
from app.account import Account
@withdraw_money_bp.route('/withdraw_money/get_account_info', methods=['POST'])
def get_account_info():
    try:
        ma_so = request.form['ma_so']
        cursor = db.get_cursor()
        query = """
            SELECT k.Ho_ten , trang_thai_tai_khoan, Loai_tiet_kiem, Tien_nap_ban_dau,Lai_suat
            FROM Tai_khoan_tiet_kiem t
            JOIN Khach_hang k ON t.Nguoi_so_huu = k.Chung_minh_Thu
            WHERE t.ID_tai_khoan = %s
        """
        cursor.execute(query, (ma_so,))
        result = cursor.fetchone()
        
        # ngay_mo = get_open_date(ma_so)
        # ngay_rut = request.form['ngay_rut']
        # expired_time = cal_expired_time(ngay_mo, ngay_rut, result[2])
        old_balance = calculate_old_balance(ma_so, result[4], 1, result[2])

        if result:
            return jsonify({'ten_tai_khoan': result[0],
                            'Trang_thai_tai_khoan': result[1],
                            'loai_tiet_kiem': result[2],
                            'Tien_nap_ban_dau':result[3],
                            'Lai_suat': result[4],
                            'old_balance' : old_balance,
                            }
                            ), 200
        else:
            return jsonify({'message': 'Account information not found.'}), 404

    except Exception as e:
        return jsonify({'message': 'An error has occurred.', 'error': str(e)}), 500
@withdraw_money_bp.route('/withdraw_money/get_old_balance', methods=['POST'])
def get_old_balance():
    try:
        ma_so = request.form['ma_so']
        rate = get_rate_by_id(ma_so)
        old_balance = calculate_old_balance(ma_so, rate)
        if old_balance:
            return jsonify({'Old balance': old_balance}), 200
        else:
            return jsonify({'message': 'Account information not found.'}), 404

    except Exception as e:
        return jsonify({'message': 'An error has occurred.', 'error': str(e)}), 500
@withdraw_money_bp.route('/withdraw_money/get_interest_money', methods=['POST'])
def get_interest_money():
    try:
        ma_so = request.form['ma_so']
        account = Account(ma_so)
        interest_money = account.get_interest_rate_money()
        if interest_money:
            return jsonify({'Interest_money': interest_money}), 200
        else:
            return jsonify({'message': 'Account information not found.'}), 404

    except Exception as e:
        return jsonify({'message': 'An error has occurred.', 'error': str(e)}), 500

@withdraw_money_bp.route('/withdraw_money')
def withdraw_money():
    return render_template('withdraw_money/withdraw_money.html',regulation=regulation)

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
        errors.append('The withdrawal date cannot be later than the current date.')
        
    if ngay_rut < ngay_mo:
        errors.append('The withdrawal date cannot be earlier than the account opening date.')
    return errors

def validate_withdraw_balance(term, so_tien_rut, old_balance):
    errors = []
    if term == 'no period':
        if int(so_tien_rut) > int(old_balance):
            errors.append('The withdrawal amount cannot be greater than the current balance.')
    elif term == '3 months':
        if int(so_tien_rut) != int(old_balance):
            errors.append('The 3-month fixed savings account must be fully withdrawn.')
    elif term == '6 months':
        if int(so_tien_rut) != int(old_balance):
            errors.append('The 6-month fixed savings account must be fully withdrawn.')
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

def validate_date (ngay_giao_dich, ngay_mo):
    errors = []
    current_date = datetime.now().date()
    minimum_withdraw_date = regulation.get_minimum_withdraw_day()
    if (ngay_giao_dich != None and current_date < ngay_giao_dich + timedelta(days=minimum_withdraw_date)) or (ngay_giao_dich == None and current_date < ngay_mo + timedelta(days=minimum_withdraw_date)):
        errors.append('Withdrawals can only be made at least 15 days after the most recent transaction.')
    return errors
    
def get_term(ma_so, errors):
    # Lấy loại tiết kiệm từ mã số 
    cursor = db.get_cursor()
    query = "SELECT Loai_tiet_kiem FROM Tai_khoan_tiet_kiem WHERE ID_tai_khoan = %s"
    cursor.execute(query, (ma_so,))
    result = cursor.fetchone()
    if not result:
        errors.append('Account information not found.')

    return result[0] if result else None
 
def save_data_to_database(ma_so, ngay_rut, so_tien_rut):
    cursor = db.get_cursor()
    print ("9")
    # Tạo ID giao dịch mới
    query = "SELECT MAX(SUBSTRING(ID_giao_dich, 3)) FROM Giao_dich Where Loai_giao_dich = 'Withdraw' "
    cursor.execute(query)

    max_id = cursor.fetchone()[0]
    print ("id: " , max_id)
    next_id = 1 if max_id is None else int(max_id) + 1
    print ("id: " , next_id)
    new_id = f'RT{next_id:05d}'
    print ("id: " , new_id)
    
    # Lưu giao dịch mới
    insert_query = """
    INSERT INTO Giao_dich (ID_giao_dich, Tai_khoan_giao_dich, Loai_giao_dich, So_tien_giao_dich, Ngay_giao_dich)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (new_id, ma_so, 'Withdraw', so_tien_rut, ngay_rut)
    cursor.execute(insert_query, values)
    db.connection.commit()
    
def calculate_old_balance (ma_so, interest_rate, expired_time, term):
    month = 1
    if term == '3 months':
        month = 3
    elif term == '6 months':
        month = 6
        
    old_balance = 0
    cursor = db.get_cursor()
    query = """
    SELECT 
        t.Tien_nap_ban_dau,
        IFNULL(SUM(CASE WHEN g.Loai_giao_dich = 'Deposit' THEN g.So_tien_giao_dich ELSE 0 END), 0) AS Tong_tien_nap,
        IFNULL(SUM(CASE WHEN g.Loai_giao_dich = 'Withdraw' THEN g.So_tien_giao_dich ELSE 0 END), 0) AS Tong_tien_rut
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
        old_balance = float(result[0]) + float(result[1]) - float(result[2])/(1 + ((interest_rate/100) * month * expired_time))
    cursor.close()
    return old_balance

def calculate_nearest_transaction(ma_so):
    ngay_giao_dich = None
    cursor = db.get_cursor()
    query = """
    SELECT MAX(Ngay_giao_dich) AS ngay_giao_dich_moi_nhat
    FROM Giao_dich
    WHERE Tai_khoan_giao_dich = %s AND Loai_giao_dich = N'Deposit'
    """

    cursor.execute(query, (ma_so,))
    result = cursor.fetchone()
    if result and result[0]:
        ngay_giao_dich = result[0]

    cursor.close()
    return ngay_giao_dich
    
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
    
def set_close_day(ma_so):
    cursor = db.get_cursor()
    query = """
    UPDATE Tai_khoan_tiet_kiem
    SET Trang_thai_tai_khoan = 0, Ngay_dong = CURDATE()
    WHERE ID_tai_khoan = %s;
    """
    cursor.execute(query, (ma_so,))
    db.connection.commit()
    
def cal_withdraw_money(term, so_tien_rut, rate, expired_time):
    month = 1
    if term == '3 months':
        month = 3
    elif term == '6 months':
        month = 6
    money = int(so_tien_rut) + int(so_tien_rut) * rate/100 * expired_time * month
    return money

def cal_expired_time(ngay_mo, ngay_rut, term):
    # Tính số ngày giữa hai ngày
    delta = ngay_rut - ngay_mo
    expire_time = 1

    # Tính toán expired time theo term
    if term == '3 months':
        expire_time = int(delta.days / (3 * 30))  # Sử dụng 3*30 ngày cho 3 tháng
    elif term == '6 months':
        expire_time = int(delta.days / (6 * 30))  # Sử dụng 6*30 ngày cho 6 tháng
    return expire_time
    
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

@withdraw_money_bp.route('/withdraw_money/submit', methods=['POST'])
def submit_form2():
    try:
        print(request.form)
        ma_so = request.form['ma_so']
        ngay_rut = request.form['ngay_rut']
        so_tien = request.form['so_tien_rut']
        ngay_rut = datetime.strptime(ngay_rut, '%Y-%m-%d').date()
        ngay_mo = get_open_date(ma_so)
        so_tien_rut = so_tien.replace(',', '')
        # Kiểm tra sổ đóng 
        status = []
        if int(account_status(ma_so)) == 0:
            status.append('Account is closed')
            return jsonify({'message': 'An error has occurred.', 'errors': status}), 401
        print ("1")
        # Kiểm tra dữ liệu đầu vào ( ngày hiện tại / quá khứ và không trước ngày mở)
        input_errors = validate_input(ngay_rut, ngay_mo)
        if input_errors:
            return jsonify({'message': 'An error has occurred.', 'errors': input_errors}), 402
        print ("2")

        # Truy vấn để lấy loại tiết kiệm từ mã số ( có tồn tại mã số đó )
        term_errors = [] 
        term = get_term(ma_so, term_errors)
        if term_errors:
            return jsonify({'message': 'An error has occurred.', 'errors': term_errors}), 403
        print ("3")

        # Kiểm tra điều kiện 15 ngày ( cách ngày mở / ngày giao dịch nạp gần nhất 15 ngày)
        nearest_transaction = calculate_nearest_transaction(ma_so)
        date_errors = validate_date(nearest_transaction, ngay_mo)    
        if date_errors:
            return jsonify({'message': 'An error has occurred.', 'errors': date_errors}), 404
        
        # Tính lãi suất
        withdraw_money_after = 0
        interest_rate = validate_interest_rate(term, ngay_mo, ngay_rut)
        if interest_rate != 0:
            expired_time = cal_expired_time(ngay_mo, ngay_rut, term)
            withdraw_money_after = cal_withdraw_money(term, so_tien_rut, interest_rate, expired_time)
        else:
            interest_rate_error = ['The savings account has not met the minimum time required for withdrawal.']
            return jsonify({'message': 'An error has occurred.', 'errors': interest_rate_error}), 405
        
        # Kiểm tra thỏa điều kiện rút (Đủ tháng + Số dư)
        old_balance = calculate_old_balance(ma_so, interest_rate, expired_time, term)
        balance_errors = validate_withdraw_balance(term, so_tien_rut, old_balance)
        if balance_errors:
            return jsonify({'message': 'An error has occurred.', 'errors': balance_errors}), 406

        # Lưu vào database
        print (ma_so)
        print (ngay_rut)
        print (withdraw_money_after)
        save_data_to_database(ma_so, ngay_rut, withdraw_money_after)
        # Trường hợp rút toàn bộ => đóng sổ
        print("8")

        remaining = calculate_old_balance(ma_so, interest_rate, expired_time, term)
        print("7")
        if int(remaining) == 0:
            set_close_day(ma_so)
            
        return jsonify({'message': 'The data has been received and successfully saved.'}), 200
    except Exception as e:
        return jsonify({'message': 'An error has occurred.', 'error': str(e)}), 500

