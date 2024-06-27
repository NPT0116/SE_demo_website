from flask import render_template, request, jsonify
from datetime import datetime
from . import update_regulation_bp
from app.regulation import regulation

@update_regulation_bp.route('/update_regulation', methods=['GET'])
def update_regulation():
    try:
        return render_template('update_regulation.html', regulation=regulation)
    except Exception as e:
        raise ValueError(str(e))

@update_regulation_bp.route('/update_regulation/submit', methods=['POST'])
def submit_update_regulation():
    try:
        new_period = request.form.get('new_period')
        new_minimum = request.form.get('new_minimum')
        minimum_day = request.form.get('minimum_day')
        interest_period = request.form.get('interest_period')
        interest_rate = request.form.get('interest_rate')

        if new_period:
            regulation.add_period(new_period)
        if new_minimum:
            regulation.set_minimum_deposit_money(int(new_minimum))
        if minimum_day:
            regulation.set_minimum_withdraw_day(int(minimum_day))
        if interest_period and interest_rate:
            regulation.set_interest_rate(interest_period, float(interest_rate))
        
        periods = regulation.get_periods()
        minimum_deposit_money = regulation.get_minimum_deposit_money()
        minimum_withdraw_day = regulation.get_minimum_withdraw_day()
        interest_rates = {period: regulation.get_interest_rate(period) for period in periods}
        
        print("Periods: ", periods)
        print("Minimum Deposit: ", minimum_deposit_money)
        print("Minimum Withdraw Day: ", minimum_withdraw_day)
        print("Interest Rates: ", interest_rates)
        
        return jsonify({'message': 'Dữ liệu regulation cập nhật thành công'})
    except Exception as e:
        return jsonify({'message': 'Không thể cập nhật regulation', 'error': str(e)})
