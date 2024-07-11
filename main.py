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

@app.route('/view_account_transaction')
def view_account_transaction():
    account_id = request.args.get('ID');
    sort = request.args.get('sort', 'ID_tai_khoan')
    order = request.args.get('order', 'asc')

    # Ánh xạ các cột hợp lệ để tránh SQL injection
    valid_columns = {
        'STT': 'ID_tai_khoan',
        'Mã Số': 'ID_tai_khoan',  # Giả sử mã số là ID_tai_khoan
        'Khách Hàng': 'Ho_ten',
        'Loại Giao Dịch': 'Loai_giao_dich',
        'Số tiền giao dịch': 'So_tien_giao_dich',
        'Ngày Giao Dịch': 'Ngay_giao_dich'
    }

    # Kiểm tra xem cột sort có hợp lệ không
    if sort not in valid_columns:
        sort = 'STT'

    try:
        order_by = f"{valid_columns[sort]} {order.upper()}"
        query = f"""select ID_tai_khoan, Ho_ten, Loai_giao_dich, So_tien_giao_dich, Ngay_giao_dich from giao_dich gd
        join tai_khoan_tiet_kiem tk on gd.Tai_khoan_giao_dich = tk.ID_tai_khoan
        join khach_hang kh on tk.Nguoi_so_huu = kh.Chung_minh_thu
        where Tai_khoan_giao_dich = '{account_id}'
        ORDER BY {order_by};"""
        cursor = db.get_cursor()
        cursor.execute(query)
        accounts = cursor.fetchall()
        print ("accounts: ", accounts)
        
        return render_template('view_account_transaction.html', accounts=accounts, ID_returned = account_id)
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)})
if __name__ == '__main__':
    app.run(debug=True)
