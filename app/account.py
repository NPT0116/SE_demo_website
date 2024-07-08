from app.database import db
from mysql.connector import Error

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
    
    def __str__(self):
        return (f"Account(ID_tai_khoan={self.ID_tai_khoan}, Trang_thai_tai_khoan={self.Trang_thai_tai_khoan}, "
                f"Ngay_mo={self.Ngay_mo}, Ngay_dong={self.Ngay_dong}, Nguoi_so_huu={self.Nguoi_so_huu}, "
                f"Loai_tiet_kiem={self.Loai_tiet_kiem}, Tien_nap_ban_dau={self.Tien_nap_ban_dau}, Lai_suat={self.Lai_suat})")
