from flask import render_template, request, jsonify
from app.database import db

from . import view_accounts_bp


@view_accounts_bp.route('/view_accounts')
def view_accounts():
    sort = request.args.get('sort', 'ID_tai_khoan')
    order = request.args.get('order', 'asc')

    # Ánh xạ các cột hợp lệ để tránh SQL injection
    valid_columns = {
        'ID': 'ID_tai_khoan',
        'Account Number': 'ID_tai_khoan',  # Giả sử mã số là ID_tai_khoan
        'Customer': 'Ho_ten',
        'Account Type': 'Loai_tiet_kiem',
        'Initial Amount': 'Tien_nap_ban_dau',
        'Interest Rate': 'Lai_suat',
        'Current Amount': 'Tong_tien'
    }

    # Kiểm tra xem cột sort có hợp lệ không
    if sort not in valid_columns:
        sort = 'ID'

    try:
        order_by = f"{valid_columns[sort]} {order.upper()}"
        query = f"""SELECT ID_tai_khoan, Ho_ten, Loai_tiet_kiem, Tien_nap_ban_dau, Tien_Lai, Lai_suat,
COALESCE(Tien_nap_ban_dau + Tien_Lai, ((Select SUM(So_tien_giao_dich) from giao_dich gd where gd.Tai_khoan_giao_dich = ID_tai_khoan and gd.Loai_giao_dich = 'Nạp Tiền') 
- (Select SUM(So_tien_giao_dich) from giao_dich gd where gd.Tai_khoan_giao_dich = ID_tai_khoan and gd.Loai_giao_dich = 'Rút Tiền') + Tien_nap_ban_dau)) as Tong_tien, Trang_thai_tai_khoan
FROM (
    SELECT tk.ID_tai_khoan, kh.Ho_ten, tk.Loai_tiet_kiem, tk.Tien_nap_ban_dau, 
           DATEDIFF(CURDATE(), tk.Ngay_mo)*tk.Lai_suat*tk.Tien_nap_ban_dau/(30*100) as Tien_Lai, 
           tk.Lai_suat , tk.Trang_thai_tai_khoan  
            FROM tai_khoan_tiet_kiem tk
            JOIN khach_hang kh ON tk.Nguoi_so_huu = kh.Chung_minh_thu
            WHERE Loai_tiet_kiem != N'Không kỳ hạn'

            UNION 

            SELECT tk.ID_tai_khoan, kh.Ho_ten, tk.Loai_tiet_kiem, tk.Tien_nap_ban_dau, Null as Tien_Lai, tk.Lai_suat, tk.Trang_thai_tai_khoan 
            FROM tai_khoan_tiet_kiem tk
            JOIN khach_hang kh ON tk.Nguoi_so_huu = kh.Chung_minh_thu
            WHERE Loai_tiet_kiem = N'Không kỳ hạn' 
        ) AS combined_results
        ORDER BY {order_by};"""
        cursor = db.get_cursor()
        cursor.execute(query)
        accounts = cursor.fetchall()
        
        if (sort == 'Tổng Tiền Hiện Tại'):
            is_tong_tien = False;
        else :
            is_tong_tien = True;
        
        return render_template('view_accounts/view_accounts.html', accounts=accounts, show_initial_amount = is_tong_tien)
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)})
    

@view_accounts_bp.route('/view_account_transaction', methods=['GET'])
def view_account_transaction():
    account_id = request.args.get('ID')
    sort = request.args.get('sort', 'ID_tai_khoan')
    order = request.args.get('order', 'asc')

    # Ánh xạ các cột hợp lệ để tránh SQL injection
    valid_columns = {
        'No.': 'Ngay_giao_dich',
        'Transaction Type': 'Loai_giao_dich',
        'Transaction Amount': 'So_tien_giao_dich',
        'Transaction Date': 'Ngay_giao_dich'
    }

    # Kiểm tra xem cột sort có hợp lệ không
    if sort not in valid_columns:
        sort = 'Transaction Date'

    try:
        order_by = f"{valid_columns[sort]} {order.upper()}"
        
        # Truy vấn thông tin tài khoản
        account_query = f"""
        SELECT tk.ID_tai_khoan, kh.Ho_ten, tk.Loai_tiet_kiem, tk.Ngay_mo, COALESCE(tk.Ngay_dong, N'Tài khoản còn hoạt động')
        FROM tai_khoan_tiet_kiem tk
        JOIN khach_hang kh ON kh.Chung_minh_thu = tk.Nguoi_so_huu
        WHERE tk.ID_tai_khoan = '{account_id}'
        """
        cursor = db.get_cursor()
        cursor.execute(account_query)
        account = cursor.fetchone()

        # Truy vấn thông tin giao dịch
        transaction_query = f"""
        SELECT  Loai_giao_dich, So_tien_giao_dich, Ngay_giao_dich FROM giao_dich gd
        JOIN tai_khoan_tiet_kiem tk ON gd.Tai_khoan_giao_dich = tk.ID_tai_khoan
        JOIN khach_hang kh ON tk.Nguoi_so_huu = kh.Chung_minh_thu
        WHERE Tai_khoan_giao_dich = '{account_id}'
        ORDER BY {order_by}
        """
        cursor.execute(transaction_query)
        transactions = cursor.fetchall()
        
        
        return render_template('view_accounts/view_account_transaction.html', account=account, Transactions=transactions, ID_returned=account_id)
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)})