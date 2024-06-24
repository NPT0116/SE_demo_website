from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime
    
app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Npt16012004",
    database="saving_account_management"
)

cursor = db.cursor()
try:
    cursor.execute("SELECT VERSION();")  # Truy vấn đơn giản để kiểm tra kết nối
    version = cursor.fetchone()
    print("Database version:", version[0])
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form1')
def form1():
    return render_template('form1.html')

@app.route('/form2')
def form2():
    return render_template('form2.html')



@app.route('/submit_form1', methods=['POST'])
def submit_form1():
    try:
        # Xử lý dữ liệu nhận được từ form
        ma_so = request.form['ma_so']
        loai_tiet_kiem = request.form['loai_tiet_kiem']
        khach_hang = request.form['khach_hang']
        cmnd = request.form['cmnd']
        dia_chi = request.form['dia_chi']
        ngay_mo_so = request.form['ngay_mo_so']
        so_tien_gui = request.form['so_tien_gui']
        ngay_mo_so = datetime.strptime(ngay_mo_so, '%Y-%m-%d').date()

        # Truy vấn để chèn dữ liệu vào bảng
        query = """
        INSERT INTO create_account (ma_so, loai_tiet_kiem, khach_hang, cmnd, dia_chi, ngay_mo_so, so_tien_gui)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (ma_so, loai_tiet_kiem, khach_hang, cmnd, dia_chi, ngay_mo_so, so_tien_gui)
        
        cursor.execute(query, values)
        db.commit()  # Đảm bảo rằng giao dịch được ghi vào cơ sở dữ liệu
        print ("Ghi xuống DB thành công.")
        return jsonify({'message': 'Dữ liệu đã được gửi và lưu thành công'})
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return jsonify({'message': 'Failed to insert data into database', 'error': str(err)})
    except Exception as e:
        print("An error occurred: {}".format(e))
        return jsonify({'message': 'An error occurred', 'error': str(e)})

@app.route('/submit_form2', methods=['POST'])
def submit_form2():
    # Xử lý dữ liệu nhận được từ form
    data = request.form
    print(data)  # In dữ liệu ra console để debug

    # Trả về phản hồi JSON
    return jsonify({'message': 'Dữ liệu đã được nhận thành công'})

@app.route('/view_accounts')
def view_accounts():
    try:
        query = "SELECT id, ma_so, loai_tiet_kiem, khach_hang, cmnd, dia_chi, DATE_FORMAT(ngay_mo_so, '%d-%m-%Y') as ngay_mo_so, so_tien_gui FROM create_account"
        cursor.execute(query)
        accounts = cursor.fetchall()
        return render_template('view_accounts.html', accounts=accounts)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return jsonify({'message': 'Failed to retrieve data from database', 'error': str(err)})



if __name__ == '__main__':
    app.run(debug=True)
