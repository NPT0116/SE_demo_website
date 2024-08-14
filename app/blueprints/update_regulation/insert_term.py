from flask import Blueprint, render_template, request, jsonify
from app.regulation import regulation
from app.database import db
insert_term_bp = Blueprint('insert_term', __name__)

@insert_term_bp.route('/insert_term', methods=['GET'])
def insert_term():
    return render_template('update_regulation/insert_term.html')

@insert_term_bp.route('/insert_term/submit', methods=['POST'])
def submit_insert_term():
    try:
        new_period = request.form.get('term')
        new_interest = request.form.get('interest')

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
@insert_term_bp.route('/term_list', methods=['GET'])
def list_term():
    return render_template("update_regulation/term.html")
@insert_term_bp.route('/get_term_list', methods=['GET'])
def get_list_term():
    try:
        # Get all terms and interest rates from the database
        query = "SELECT term_name, interest_rate FROM terms"
        cursor = db.get_cursor()
        terms = []

        if cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            for row in results:
                terms.append({
                    'term_name': row[0],
                    'interest_rate': row[1]
                })
            cursor.close()

        # Return as a JSON response
        return jsonify(terms), 200
    except Exception as e:
        print(f"Error fetching terms: {e}")
        return jsonify({'error': 'Failed to fetch terms'}), 500