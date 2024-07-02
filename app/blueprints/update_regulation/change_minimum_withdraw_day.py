from flask import Blueprint, render_template, request, jsonify
from app.regulation import regulation

change_minimum_withdraw_day_bp = Blueprint('change_minimum_withdraw_day', __name__)

@change_minimum_withdraw_day_bp.route('/change_minimum_withdraw_day', methods=['GET'])
def change_minimum_withdraw_day():
    return render_template('update_regulation/change_minimum_withdraw_day.html')

@change_minimum_withdraw_day_bp.route('/change_minimum_withdraw_day/submit', methods=['POST'])
def submit_change_minimum_withdraw_day():
    minimum_day = int(request.form.get('minimum_day'))
    regulation.add_minimum_withdraw_day(minimum_day)
    return jsonify({'message': 'Số ngày rút tối thiểu đã được cập nhật thành công'})
