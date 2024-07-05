from flask import render_template, request, jsonify
from app.database import db

from . import view_accounts_bp


@view_accounts_bp.route('/view_accounts')
def view_accounts():
    try:
        query = "select ID_tai_khoan, Ho_ten, loai_tiet_kiem, tien_nap_ban_dau from tai_khoan_tiet_kiem tktk join khach_hang kh on tktk.Nguoi_so_huu = kh.chung_Minh_thu"
        cursor = db.get_cursor()
        cursor.execute(query)
        accounts = cursor.fetchall()
        print ("accounts: ", accounts)
        return render_template('view_accounts.html', accounts=accounts)
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)})
    
