from flask import render_template, request, jsonify
from app.database import db

from . import view_accounts_bp


@view_accounts_bp.route('/view_accounts')
def view_accounts():
    try:
        query = "SELECT ID_tai_khoan,  Loai_tiet_kiem, Ho_ten, Tien_nap_ban_dau FROM Tai_khoan_tiet_kiem tktk join Khach_hang kh on kh.ID_khach_hang = tktk.Nguoi_so_huu "
        cursor = db.get_cursor()
        cursor.execute(query)
        accounts = cursor.fetchall()
        print ("accounts: ", accounts)
        return render_template('view_accounts.html', accounts=accounts)
    except Exception as e:
        return jsonify({'message': 'An error occurred', 'error': str(e)})
    
