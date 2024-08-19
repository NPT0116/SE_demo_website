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


if __name__ == '__main__':
    app.run(debug=True)
