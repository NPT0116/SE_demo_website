from flask import render_template, request, jsonify
from app.database import db


# Kết nối cơ sở dữ liệu

from . import withdraw_money_bp

@withdraw_money_bp.route('/withdraw_money')
def withdraw_money():
    return render_template('withdraw_money.html')

@withdraw_money_bp.route('/withdraw_money/submit', methods=['POST'])
def submit_form2():
    try:
        # Xử lý dữ liệu nhận được từ form
        data = request.form
        print(data)  # In dữ liệu ra console để debug

        # Thực hiện xử lý và lưu trữ dữ liệu từ form2 (thêm phần này nếu cần)
        
        return jsonify({'message': 'Dữ liệu đã được nhận thành công'})
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)})
