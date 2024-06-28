from flask import Blueprint, render_template
from app.regulation import regulation
insert_term_bp = Blueprint('insert_term', __name__)

@insert_term_bp.route('/insert_term', methods=['GET'])
def insert_term():
    return render_template('insert_term.html')

@insert_term_bp.route('/insert_term/submit', methods=['POST'])
def submit_insert_term():
    new_period = request.form.get('new_period')
    regulation.add_period(new_period)
    return jsonify({'message': 'Kỳ hạn mới đã được thêm thành công'})
