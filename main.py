from flask import Flask, render_template, jsonify, request
from app.blueprints.register_account import register_account_bp  
from app.blueprints.deposit_money import deposit_money_bp 
from app.blueprints.view_accounts import view_accounts_bp 
from app.blueprints.update_regulation import update_regulation_bp 
from app.blueprints.withdraw_money import withdraw_money_bp  
from app.blueprints.report import report_bp
from app.blueprints.home import home_bp
from app.account import Account
from app.database import db
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Đăng ký các Blueprints với ứng dụng chính
app.register_blueprint(register_account_bp)
app.register_blueprint(deposit_money_bp)
app.register_blueprint(view_accounts_bp)
app.register_blueprint(update_regulation_bp, url_prefix = '/regulation')
app.register_blueprint(withdraw_money_bp)
app.register_blueprint(report_bp, url_prefix='/report')
app.register_blueprint(home_bp)

@app.route('/account')
def account():
    return render_template('account.html')
@app.route('/account/<maSo>')
def account_detail(maSo):
    account = Account(maSo)
    account_data = {
        'ID_tai_khoan': account.ID_tai_khoan,
        'Trang_thai_tai_khoan': account.Trang_thai_tai_khoan,
        'Ngay_mo': account.get_date_format(),
        'Ngay_dong': account.Ngay_dong,
        'Nguoi_so_huu': account.Nguoi_so_huu,
        'Loai_tiet_kiem': account.Loai_tiet_kiem,
        'Tien_nap_ban_dau': account.Tien_nap_ban_dau,
        'Lai_suat': account.Lai_suat,
        'Thoi-Gian-toi-hien-tai': account.get_day_diff(),
        'Tien_lai': account.get_interest_rate_money()
    }
    return jsonify(account_data)

@app.route('/view_account_transaction', methods=['GET'])
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
if __name__ == '__main__':
    app.run(debug=True)
