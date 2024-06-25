from flask import render_template, request, jsonify
from app.database import db

from . import view_accounts_bp


@view_accounts_bp.route('/view_accounts')
def view_accounts():
    try:
        query = "SELECT id, ma_so, loai_tiet_kiem, khach_hang, cmnd, dia_chi, DATE_FORMAT(ngay_mo_so, '%d-%m-%Y') as ngay_mo_so, so_tien_gui FROM create_account"
        cursor = db.get_cursor()
        cursor.execute(query)
        accounts = cursor.fetchall()
        return render_template('view_accounts.html', accounts=accounts)
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)})