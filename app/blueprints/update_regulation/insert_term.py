from flask import Blueprint, render_template, request, jsonify
from app.regulation import regulation

insert_term_bp = Blueprint('insert_term', __name__)

@insert_term_bp.route('/insert_term', methods=['GET'])
def insert_term():
    return render_template('update_regulation/insert_term.html')

@insert_term_bp.route('/insert_term/submit', methods=['POST'])
def submit_insert_term():
    try:
        new_period = request.form.get('new_period')
        new_interest = request.form.get('new_interest')

        print(new_interest)
        if new_period:
            regulation.add_term(new_period)
            if new_interest:
                regulation.update_interest_rate(new_period, new_interest)
            return jsonify({'message': 'Kỳ hạn mới đã được thêm thành công'})
        else:
            return jsonify({'message': 'Kỳ hạn mới không được bỏ trống'}), 400
    except Exception as e:
        return jsonify({'message': 'Có lỗi xảy ra', 'error': str(e)}), 500
