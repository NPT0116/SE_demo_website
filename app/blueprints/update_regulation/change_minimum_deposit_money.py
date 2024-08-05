from flask import Blueprint, render_template, request, jsonify
from app.regulation import regulation

change_minimum_deposit_money_bp = Blueprint('change_minimum_deposit_money', __name__)

@change_minimum_deposit_money_bp.route('/change_minimum_deposit_money', methods=['GET'])
def change_minimum_deposit_money():
    return render_template('update_regulation/change_minimum_deposit_money.html')
@change_minimum_deposit_money_bp.route('/change_minimum_deposit_money/get_current', methods=['GET'])
def get_currrent_minimum_deposit_money():
    current = regulation.get_minimum_deposit_money()
    return jsonify({'current money': current})

@change_minimum_deposit_money_bp.route('/change_minimum_deposit_money/submit', methods=['POST'])
def submit_change_minimum_deposit_money():
    new_minimum = int(request.form.get('minimum_deposit'))
    if new_minimum:
        regulation.add_minimum_deposit_money(new_minimum)
    else: 
        print ("can't submit blank content")
    return jsonify({'message': 'Số tiền gửi tối thiểu đã được cập nhật thành công'})
