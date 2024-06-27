from flask import render_template, request, jsonify
from datetime import datetime
from . import update_regulation_bp
from app.regulation import regulation


@update_regulation_bp.route('/update_regulation',methods=['GET'])
def update_regulation():
    try:
        return render_template('update_regulation.html')
    except Exception as e:
        raise ValueError (str(e))

@update_regulation_bp.route('/update_regulation/submit', methods = ['POST'])
def submit_update_regulation():
    try:
        new_period = request.form.get('new_period')
        new_minimum = request.form.get('new_minimum')

        if new_period:
            regulation.add_period(new_period, 0)  # Thêm với lãi suất mặc định
        if new_minimum:
            regulation.set_minimum_deposit_money(int(new_minimum))

        periods = regulation.get_periods()  # Gọi phương thức để lấy giá trị
        minimum_deposit_money = regulation.get_minimum_deposit_money()     
        print("Periods:", periods)
        print("Minimum Deposit Money:", minimum_deposit_money)
        return jsonify({'message': 'Dữ liệu regulation cập nhật thành công'})
    except Exception as e:
        return jsonify({'message': 'Không thể cập nhật regulation', 'error': str(e)})