from flask import render_template, request, jsonify
from app.database import db


# Kết nối cơ sở dữ liệu

from . import deposit_money_bp

@deposit_money_bp.route('/deposit_money')
def deposit_money():
    return render_template('deposit_money.html')

@deposit_money_bp.route('/submit_deposit_money', methods=['POST'])
def submit_form2():
    try:
        # Xử lý dữ liệu nhận được từ form
        data = request.form
        print(data)  # In dữ liệu ra console để debug

        # Thực hiện xử lý và lưu trữ dữ liệu từ form2 (thêm phần này nếu cần)
        
        return jsonify({'message': 'Dữ liệu đã được nhận thành công'})
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)})
