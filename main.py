from flask import Flask, render_template
from app.blueprints.register_account import register_account_bp  # Import Blueprint từ module form1
from app.blueprints.deposit_money import deposit_money_bp  # Import Blueprint từ module form2 (tạo tương tự như form1)

app = Flask(__name__)

# Đăng ký các Blueprints với ứng dụng chính
app.register_blueprint(register_account_bp)
app.register_blueprint(deposit_money_bp)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view_accounts')
def view_accounts():
    try:
        query = "SELECT id, ma_so, loai_tiet_kiem, khach_hang, cmnd, dia_chi, DATE_FORMAT(ngay_mo_so, '%d-%m-%Y') as ngay_mo_so, so_tien_gui FROM create_account"
        cursor = db.get_cursor()
        cursor.execute(query)
        accounts = cursor.fetchall()
        return render_template('view_accounts.html', accounts=accounts)
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
