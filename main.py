from flask import Flask, render_template
from app.blueprints.register_account import register_account_bp  
from app.blueprints.deposit_money import deposit_money_bp 
from app.blueprints.view_accounts import view_accounts_bp 
from app.blueprints.update_regulation import update_regulation_bp 
from app.blueprints.withdraw_money import withdraw_money_bp  
from app.blueprints.report import report_bp
from app.database import db
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# Đăng ký các Blueprints với ứng dụng chính
app.register_blueprint(register_account_bp)
app.register_blueprint(deposit_money_bp)
app.register_blueprint(view_accounts_bp)
app.register_blueprint(update_regulation_bp)
app.register_blueprint(withdraw_money_bp)
app.register_blueprint(report_bp, url_prefix='/report')

@app.route('/')
def home():
    return render_template('home.html')



if __name__ == '__main__':
    app.run(debug=True)
