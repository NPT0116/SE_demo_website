from flask import Blueprint, render_template, request, jsonify
from app.regulation import regulation

update_interest_rate_bp = Blueprint('update_interest_rate', __name__)

@update_interest_rate_bp.route('/update_interest_rate', methods=['GET'])
def update_interest_rate():
    return render_template('update_interest_rate.html', regulation=regulation)

@update_interest_rate_bp.route('/update_interest_rate/submit', methods=['POST'])
def submit_update_interest_rate():
    period = request.form.get('interest_period')
    rate = float(request.form.get('interest_rate'))
    regulation.set_interest_rate(period, rate)
    return jsonify({'message': 'Lãi suất đã được cập nhật thành công'})
