from app.database import db
from mysql.connector import Error
from datetime import datetime
import re

class Account:
    def __init__(self, maSo):
        self.db = db
        self.cursor = self.db.get_cursor()
        self.ID_tai_khoan = maSo
        self.Trang_thai_tai_khoan = None
        self.Ngay_mo = None
        self.Ngay_dong = None
        self.Nguoi_so_huu = None
        self.Loai_tiet_kiem = None
        self.Tien_nap_ban_dau = None
        self.Lai_suat = None
        self.load_account(maSo)
    
    def load_account(self, maSo):
        query = "SELECT * FROM Tai_khoan_tiet_kiem WHERE ID_tai_khoan = %s"
        try:
            self.cursor.execute(query, (maSo,))
            account_data = self.cursor.fetchone()
            print (account_data)
            if account_data:
                self.ID_tai_khoan = account_data[0]
                self.Trang_thai_tai_khoan = account_data[1]
                self.Ngay_mo = account_data[2]
                self.Ngay_dong = account_data[3]
                self.Nguoi_so_huu = account_data[4]
                self.Loai_tiet_kiem = account_data[5]
                self.Tien_nap_ban_dau = account_data[6]
                self.Lai_suat = account_data[7]
        except Error as e:
            print(f"Error: {e}")
    
    def update_account(self, **kwargs):
        updates = ", ".join(f"{key} = %s" for key in kwargs)
        values = list(kwargs.values())
        values.append(self.ID_tai_khoan)
        query = f"UPDATE Tai_khoan_tiet_kiem SET {updates} WHERE ID_tai_khoan = %s"
        try:
            self.cursor.execute(query, values)
            self.db.connection.commit()
            print("Account updated successfully")
            self.load_account(self.ID_tai_khoan)  # Reload the account data to update the instance variables
        except Error as e:
            print(f"Error: {e}")
    def get_name(self):
        query = "Select ho_ten from Khach_hang join Tai_khoan_tiet_kiem on Nguoi_so_huu = Chung_minh_Thu where ID_tai_khoan = %s"
        try:
            self.cursor.execute(query, (self.ID_tai_khoan,))
            name = self.cursor.fetchone()
            return name[0]
        except Error as e:
            print (f"Error: {e}")
    def close(self):
        self.db.connection.close()
    def get_date_format(self):
        date_obj = self.Ngay_mo

        formatted_date = date_obj.strftime("%d/%m/%Y")

        return formatted_date
    def get_balance(self):
        if self.Loai_tiet_kiem == "no period":
            query = "SELECT tktk.ID_tai_khoan,tktk.Tien_nap_ban_dau, COALESCE(SUM(CASE WHEN gd.Loai_giao_dich = 'Nạp Tiền' THEN gd.So_tien_giao_dich ELSE 0 END), 0) AS Tong_nap_tien,COALESCE(SUM(CASE WHEN gd.Loai_giao_dich = 'Rút Tiền' THEN gd.So_tien_giao_dich ELSE 0 END), 0) AS Tong_rut_tien,tktk.Tien_nap_ban_dau + COALESCE(SUM(CASE WHEN gd.Loai_giao_dich = 'Nạp Tiền' THEN gd.So_tien_giao_dich ELSE 0 END), 0) - COALESCE(SUM(CASE WHEN gd.Loai_giao_dich = 'Rút Tiền' THEN gd.So_tien_giao_dich ELSE 0 END), 0)/(1+tktk.lai_suat/100) AS Tong_so_tien FROM  Tai_khoan_tiet_kiem tktk LEFT JOIN Giao_dich gd ON tktk.ID_tai_khoan = gd.Tai_khoan_giao_dich WHERE tktk.loai_tiet_kiem = 'no period' and and tktk.id_tai_khoan = %s GROUP BY tktk.ID_tai_khoan, tktk.Tien_nap_ban_dau, tktk.lai_suat;"
            try:
                self.cursor.execute(query, (self.ID_tai_khoan,))
                name = self.cursor.fetchone()
                return name[2]
            except Error as e:
                print (f"Error: {e}")
        else:
            print ("Account term type must be no period to get balance")
    def get_day_diff(self):
        if self.Ngay_mo:
            current_date = datetime.now().date()
            day_diff = (current_date - self.Ngay_mo).days
            return day_diff
        else:
            return None
    def extract_number(self,term):
    # Sử dụng biểu thức chính quy để tìm phần số trong chuỗi
        match = re.search(r'\d+', term)
        if match:
            return int(match.group())
        return None
    def get_interest_rate_money(self):
        if self.Loai_tiet_kiem != 'no period':
            months = self.extract_number(self.Loai_tiet_kiem)
            expire = self.get_day_diff()//(months*30)
            print(expire)
            return (1+((float)(self.Lai_suat)/100) * expire * months) * (float)(self.Tien_nap_ban_dau)
        else:
            return self.Tien_nap_ban_dau
    def __str__(self):
        return (f"Account(ID_tai_khoan={self.ID_tai_khoan}, Trang_thai_tai_khoan={self.Trang_thai_tai_khoan}, "
                f"Ngay_mo={self.Ngay_mo}, Ngay_dong={self.Ngay_dong}, Nguoi_so_huu={self.Nguoi_so_huu}, "
                f"Loai_tiet_kiem={self.Loai_tiet_kiem}, Tien_nap_ban_dau={self.Tien_nap_ban_dau}, Lai_suat={self.Lai_suat})")
