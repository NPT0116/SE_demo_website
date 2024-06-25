from flask import Flask, render_template
from app.blueprints.register_account import register_account_bp  # Import Blueprint từ module form1
from app.blueprints.deposit_money import deposit_money_bp  # Import Blueprint từ module form2 (tạo tương tự như form1)
from app.blueprints.view_accounts import view_accounts_bp  # Import Blueprint từ module form2 (tạo tương tự như form1)
from app.database import db
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Đăng ký các Blueprints với ứng dụng chính
app.register_blueprint(register_account_bp)
app.register_blueprint(deposit_money_bp)
app.register_blueprint(view_accounts_bp)
@app.route('/')
def home():
    return render_template('home.html')



if __name__ == '__main__':
    app.run(debug=True)
