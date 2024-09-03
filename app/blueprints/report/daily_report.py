from flask import Blueprint, render_template, request, jsonify
from app.database import db

daily_report_bp = Blueprint('daily_report', __name__)

@daily_report_bp.route('/', methods=['GET'])
def daily_report():
    return render_template('report/daily_report.html')
@daily_report_bp.route('/chart', methods=['GET'])
def daily_chart():
    return render_template('report/daily_chart.html')
@daily_report_bp.route('/get_info', methods=['POST'])
def get_daily_report():
    try:
        data = request.json

        ngay = data['ngay']
        print (ngay)
        query = f"""
SELECT '{ngay}',rut_tien.Loai_tiet_kiem, nap_tien.TONG_NAP + Revernue_from_Create_account.Amount ,rut_tien.TONG_RUT
FROM
(SELECT tk.Loai_tiet_kiem, IFNULL(SUM(tk_gd.So_tien_giao_dich),0 ) as TONG_RUT
                    FROM (select Tai_khoan_giao_dich, So_tien_giao_dich from Giao_dich gd
                    where Ngay_giao_dich = '{ngay}'  and Loai_giao_dich = N'Rút tiền') as tk_gd
                    RIGHT JOIN Tai_khoan_tiet_kiem tk on tk.ID_tai_khoan = tk_gd.Tai_khoan_giao_dich
                    group by tk.Loai_tiet_kiem) as rut_tien
                    ,(SELECT tk.Loai_tiet_kiem, IFNULL(SUM(tk_gd.So_tien_giao_dich),0 )  as TONG_NAP
                    FROM (select Tai_khoan_giao_dich, So_tien_giao_dich from Giao_dich gd
                    where Ngay_giao_dich = '{ngay}' and Loai_giao_dich = N'Nạp tiền') as tk_gd
                    RIGHT JOIN Tai_khoan_tiet_kiem tk on tk.ID_tai_khoan = tk_gd.Tai_khoan_giao_dich
                    group by tk.Loai_tiet_kiem) as nap_tien
                    , (SELECT IFNULL(SUM(TAO_TK_SUM.init_am), 0) as Amount, loai_tk.Loai_tiet_kiem as type_tk  from  (SELECT TAO_TK.Tien_nap_ban_dau as init_am,ID_tai_khoan , Loai_tiet_kiem  FROM Tai_khoan_tiet_kiem as TAO_TK 
                    where TAO_TK.Ngay_mo = '{ngay}') as TAO_TK_SUM
                    RIGHT JOIN Tai_khoan_tiet_kiem as loai_tk on loai_tk.ID_tai_khoan = TAO_TK_SUM.ID_tai_khoan
                    Group by loai_tk.Loai_tiet_kiem) as Revernue_from_Create_account
                    where rut_tien.Loai_tiet_kiem = nap_tien.Loai_tiet_kiem and Revernue_from_Create_account.type_tk = nap_tien.Loai_tiet_kiem
"""
        cursor = db.get_cursor()
        cursor.execute(query)
        daily_reports = cursor.fetchall()
        result = [
            {
                "loai_tiet_kiem": row[0],
                "tong_nap": float(row[1]),
                "tong_rut": float(row[2]),
                "chenh_lech": abs(float(row[1]) - float(row[2]))
            }
            for row in daily_reports
        ]
        print (result)

        return jsonify(result)
    except Exception as e:
        return jsonify({'message': 'Không thể gửi báo cáo hàng ngày', 'error': str(e)}), 500
@daily_report_bp.route('/submit', methods=['POST'])
def submit_daily_report():
    try:
        print(request.form)
        ngay = request.form['ngay']
        print(ngay)
        query = f"""
SELECT '{ngay}',rut_tien.Loai_tiet_kiem, nap_tien.TONG_NAP + Revernue_from_Create_account.Amount ,rut_tien.TONG_RUT
FROM
(SELECT tk.Loai_tiet_kiem, IFNULL(SUM(tk_gd.So_tien_giao_dich),0 ) as TONG_RUT
                    FROM (select Tai_khoan_giao_dich, So_tien_giao_dich from Giao_dich gd
                    where Ngay_giao_dich = '{ngay}' and Loai_giao_dich = N'Rút tiền') as tk_gd
                    RIGHT JOIN Tai_khoan_tiet_kiem tk on tk.ID_tai_khoan = tk_gd.Tai_khoan_giao_dich
                    group by tk.Loai_tiet_kiem) as rut_tien
                    ,(SELECT tk.Loai_tiet_kiem, IFNULL(SUM(tk_gd.So_tien_giao_dich),0 )  as TONG_NAP
                    FROM (select Tai_khoan_giao_dich, So_tien_giao_dich from Giao_dich gd
                    where Ngay_giao_dich = '{ngay}' and Loai_giao_dich = N'Nạp tiền') as tk_gd
                    RIGHT JOIN Tai_khoan_tiet_kiem tk on tk.ID_tai_khoan = tk_gd.Tai_khoan_giao_dich
                    group by tk.Loai_tiet_kiem) as nap_tien
                    , (SELECT IFNULL(SUM(TAO_TK_SUM.init_am), 0) as Amount, loai_tk.Loai_tiet_kiem as type_tk  from  (SELECT TAO_TK.Tien_nap_ban_dau as init_am,ID_tai_khoan , Loai_tiet_kiem  FROM Tai_khoan_tiet_kiem as TAO_TK 
                    where TAO_TK.Ngay_mo = '{ngay}') as TAO_TK_SUM
                    RIGHT JOIN Tai_khoan_tiet_kiem as loai_tk on loai_tk.ID_tai_khoan = TAO_TK_SUM.ID_tai_khoan
                    Group by loai_tk.Loai_tiet_kiem) as Revernue_from_Create_account
                    where rut_tien.Loai_tiet_kiem = nap_tien.Loai_tiet_kiem and Revernue_from_Create_account.type_tk = nap_tien.Loai_tiet_kiem
"""
        cursor = db.get_cursor()
        cursor.execute(query)
        daily_reports = cursor.fetchall()
        print ("accounts: ", daily_reports)
        return render_template('report/daily_report.html', reports = daily_reports)
    except Exception as e:
        return jsonify({'message': 'Không thể gửi báo cáo hàng ngày', 'error': str(e)})