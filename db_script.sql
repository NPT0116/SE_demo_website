-- Tạo cơ sở dữ liệu QL_TAIKHOANTIETKIEM
DROP DATABASE IF EXISTS QL_TAIKHOANTIETKIEM;

CREATE DATABASE QL_TAIKHOANTIETKIEM;

-- Sử dụng cơ sở dữ liệu QL_TAIKHOANTIETKIEM
USE QL_TAIKHOANTIETKIEM;

-- Tạo bảng Khach_hang
CREATE TABLE Khach_hang (
    Ho_ten NVARCHAR(50) NOT NULL,
    Chung_minh_Thu CHAR(15) NOT NULL,
    Dia_chi NVARCHAR(80) ,
    PRIMARY KEY (Chung_minh_Thu)
);

-- Tạo bảng Tai_khoan_tiet_kiem
CREATE TABLE Tai_khoan_tiet_kiem (
    ID_tai_khoan CHAR(10) NOT NULL,
    Trang_thai_tai_khoan BOOLEAN NOT NULL DEFAULT 1,
    Ngay_mo DATE NOT NULL,
    Ngay_dong DATE DEFAULT NULL,
    Nguoi_so_huu CHAR(15) NOT NULL,
    Loai_tiet_kiem NCHAR(20) NOT NULL,
    Tien_nap_ban_dau DECIMAL(19, 4) NOT NULL,
    Lai_suat FLOAT NOT NULL,
    PRIMARY KEY (ID_tai_khoan),
    FOREIGN KEY (Nguoi_so_huu) REFERENCES Khach_hang(Chung_minh_Thu)
);

-- Tạo bảng Giao_dich
CREATE TABLE Giao_dich (
    ID_giao_dich CHAR(10) NOT NULL,
    Tai_khoan_giao_dich CHAR(10) NOT NULL,
    Loai_giao_dich NCHAR(10) NOT NULL,
    So_tien_giao_dich DECIMAL(19, 4) NOT NULL,
    Ngay_giao_dich DATE NOT NULL,
    PRIMARY KEY (ID_giao_dich),
    FOREIGN KEY (Tai_khoan_giao_dich) REFERENCES Tai_khoan_tiet_kiem(ID_tai_khoan)
);


-- Tạo bảng Regulation
CREATE TABLE IF NOT EXISTS terms (
    term_id INT AUTO_INCREMENT PRIMARY KEY,
    term_name VARCHAR(50) NOT NULL,
    interest_rate FLOAT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS minimum_deposit_money (
    id INT AUTO_INCREMENT PRIMARY KEY,
    amount INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS minimum_withdraw_day (
    id INT AUTO_INCREMENT PRIMARY KEY,
    days INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO terms (term_name, interest_rate) VALUES
('no period', 0.15),
('3 months', 0.5),
('6 months', 0.55);
INSERT INTO minimum_withdraw_day(days) Values
(15);
INSERT INTO minimum_deposit_money( amount) Values
(100000);


-- INSERT INTO Khach_hang (Ho_ten, Chung_minh_Thu, Dia_chi)
-- VALUES 
-- ( 'Lê Hoàng Đạt', '060277982156', '61/21 Liên Khu 1-6, phường Bình Trị Đông, quận Bình Tân'),
-- ( 'Phạm Quang Duy', '060277982157', '123 Nguyễn Trãi, phường Bến Thành, quận 1'),
-- ( 'Nguyễn Phúc Thành', '060277982158', '456 Lê Lợi, phường Bến Nghé, quận 1'),
-- ('Nguyễn Quang Minh', '060277982159', '789 Trần Hưng Đạo, phường Cầu Kho, quận 1');


-- Thêm các tài khoản tiết kiệm vào bảng Tai_khoan_tiet_kiem
-- INSERT INTO Tai_khoan_tiet_kiem (ID_tai_khoan, Trang_thai_tai_khoan, Ngay_mo, Ngay_dong, Nguoi_so_huu, Loai_tiet_kiem, Tien_nap_ban_dau, Lai_suat)
-- VALUES 
-- ('BT001',1, '2004-04-22',NULL, '060277982156', '3 months', 100000000, 4.6),
-- ('BT002', 1, '2023-06-15', '2023-06-18', '060277982157', '3 months', 50000000, 2.1),
-- ('ST001', 1, '2023-06-16', NULL, '060277982158', '6 months', 200000000, 4.6),
-- ('KKH001', 1,'2023-06-17', NULL,'060277982159', 'no period', 30000000, 0.15),
-- ('BT003', 1, '2023-06-18', NULL,'060277982156', '3 months', 70000000, 2.1);

-- Thêm các giao dịch vào bảng Giao_dich
-- INSERT INTO Giao_dich (ID_giao_dich, Tai_khoan_giao_dich, Loai_giao_dich, So_tien_giao_dich, Ngay_giao_dich)
-- VALUES 
-- ('RT001', 'KKH001', 'Rút Tiền', 150000000, '2024-06-30'),
-- ('NT001', 'KKH001', 'Nạp Tiền', 430000000, '2024-06-17');



DROP PROCEDURE IF EXISTS ngay_mo_so_dong_so;
DELIMITER //
CREATE PROCEDURE ngay_mo_so_dong_so(input_month VARCHAR(10), LOAITAIKHOAN NCHAR(10))
BEGIN
    DECLARE start_date DATE;
    DECLARE end_date DATE;
    DECLARE NOW_DATE DATE;

    SET start_date = STR_TO_DATE(CONCAT(input_month, '-01'), '%Y-%m-%d');
    SET end_date = LAST_DAY(start_date);

    DROP TABLE IF EXISTS temp_card_counts;
    CREATE  TABLE temp_card_counts (
        report_date DATE,
        OPEN_COUNT INT,
        CLOSE_COUNT INT
    );

    SET NOW_DATE = start_date;

    WHILE NOW_DATE <= end_date DO
        INSERT INTO temp_card_counts (report_date, OPEN_COUNT, CLOSE_COUNT)
        SELECT NOW_DATE, 
        (SELECT count(*) from Tai_khoan_tiet_kiem WHERE  Ngay_mo = NOW_DATE and Loai_tiet_kiem = LOAITAIKHOAN),
		(SELECT count(*) from Tai_khoan_tiet_kiem WHERE Ngay_dong = NOW_DATE and Loai_tiet_kiem = LOAITAIKHOAN);

        SET NOW_DATE = DATE_ADD(NOW_DATE, INTERVAL 1 DAY);
    END WHILE;

    -- Select results from temporary table
    SELECT * FROM temp_card_counts;

    -- Note: Temporary table will be automatically dropped when the session ends
END //

DELIMITER ;

select 
from tai_khoan_tiet_kiem tktk join giao_dich gd on tktk.id_tai_khoan = gd.tai_khoan_giao_dich
group by gd.tai_khoan_giao_dich


select * from terms;
select * from minimum_withdraw_day;
select * from minimum_deposit_money;

SELECT 
    tktk.ID_tai_khoan,
    tktk.Tien_nap_ban_dau,
    COALESCE(SUM(CASE WHEN gd.Loai_giao_dich = 'Nạp Tiền' THEN gd.So_tien_giao_dich ELSE 0 END), 0) AS Tong_nap_tien,
    COALESCE(SUM(CASE WHEN gd.Loai_giao_dich = 'Rút Tiền' THEN gd.So_tien_giao_dich ELSE 0 END), 0) AS Tong_rut_tien,
    tktk.Tien_nap_ban_dau + 
        COALESCE(SUM(CASE WHEN gd.Loai_giao_dich = 'Nạp Tiền' THEN gd.So_tien_giao_dich ELSE 0 END), 0) - 
        COALESCE(SUM(CASE WHEN gd.Loai_giao_dich = 'Rút Tiền' THEN gd.So_tien_giao_dich ELSE 0 END), 0)/(1+tktk.lai_suat/100) AS Tong_so_tien
FROM 
    Tai_khoan_tiet_kiem tktk
LEFT JOIN 
    Giao_dich gd ON tktk.ID_tai_khoan = gd.Tai_khoan_giao_dich
WHERE tktk.loai_tiet_kiem = 'no period'
GROUP BY 
    tktk.ID_tai_khoan, tktk.Tien_nap_ban_dau, tktk.lai_suat;
    
    
select * from tai_khoan_tiet_kiem;
select * from giao_dich;
select * from khach_hang;

SELECT MAX(SUBSTRING(ID_giao_dich, 3)) FROM Giao_dich Where Loai_giao_dich = 'Rút Tiền' 




-- Giả sử đã có các khách hàng (từ ID '060277982156' đến '060277982165') và các loại tiết kiệm ( 'no period', '3 months', '6 months') đã có sẵn trong cơ sở dữ liệu

-- Tạo thêm 20 sổ mở vào tháng 7 năm 2024
INSERT INTO Tai_khoan_tiet_kiem (ID_tai_khoan, Trang_thai_tai_khoan, Ngay_mo, Ngay_dong, Nguoi_so_huu, Loai_tiet_kiem, Tien_nap_ban_dau, Lai_suat)
VALUES 
('STK00051', 1, '2024-07-01', NULL, '060277982156', 'no period', 1000000, 0.15),
('STK00052', 1, '2024-07-02', NULL, '060277982157', '3 months', 2000000, 0.5),
('STK00053', 1, '2024-07-03', NULL, '060277982158', '6 months', 3000000, 0.55),
('STK00054', 1, '2024-07-04', NULL, '060277982159', 'no period', 4000000, 0.15),
('STK00055', 1, '2024-07-05', NULL, '060277982160', '3 months', 5000000, 0.5),
('STK00056', 1, '2024-07-06', NULL, '060277982161', '6 months', 6000000, 0.55),
('STK00057', 1, '2024-07-07', NULL, '060277982162', 'no period', 7000000, 0.15),
('STK00058', 1, '2024-07-08', NULL, '060277982163', '3 months', 8000000, 0.5),
('STK00059', 1, '2024-07-09', NULL, '060277982164', '6 months', 9000000, 0.55),
('STK00060', 1, '2024-07-10', NULL, '060277982165', 'no period', 10000000, 0.15),
('STK00061', 1, '2024-07-11', NULL, '060277982156', '3 months', 11000000, 0.5),
('STK00062', 1, '2024-07-12', NULL, '060277982157', '6 months', 12000000, 0.55),
('STK00063', 1, '2024-07-13', NULL, '060277982158', 'no period', 13000000, 0.15),
('STK00064', 1, '2024-07-14', NULL, '060277982159', '3 months', 14000000, 0.5),
('STK00065', 1, '2024-07-15', NULL, '060277982160', '6 months', 15000000, 0.55),
('STK00066', 1, '2024-07-16', NULL, '060277982161', 'no period', 16000000, 0.15),
('STK00067', 1, '2024-07-17', NULL, '060277982162', '3 months', 17000000, 0.5),
('STK00068', 1, '2024-07-18', NULL, '060277982163', '6 months', 18000000, 0.55),
('STK00069', 1, '2024-07-19', NULL, '060277982164', 'no period', 19000000, 0.15),
('STK00070', 1, '2024-07-20', NULL, '060277982165', '3 months', 20000000, 0.5);



-- Insert into Tai_khoan_tiet_kiem for July 2024 with 'no period' type starting from STK00071
INSERT INTO Tai_khoan_tiet_kiem (ID_tai_khoan, Trang_thai_tai_khoan, Ngay_mo, Ngay_dong, Nguoi_so_huu, Loai_tiet_kiem, Tien_nap_ban_dau, Lai_suat)
VALUES 
('STK00071', 1, '2024-07-01', NULL, '060277982156', 'no period', 51000000, 0.15),
('STK00072', 1, '2024-07-01', NULL, '060277982157', 'no period', 52000000, 0.15),
('STK00073', 1, '2024-07-02', NULL, '060277982158', 'no period', 53000000, 0.15),
('STK00074', 1, '2024-07-02', NULL, '060277982159', 'no period', 54000000, 0.15),
('STK00075', 1, '2024-07-03', NULL, '060277982160', 'no period', 55000000, 0.15),
('STK00076', 1, '2024-07-03', NULL, '060277982161', 'no period', 56000000, 0.15),
('STK00077', 1, '2024-07-04', NULL, '060277982162', 'no period', 57000000, 0.15),
('STK00078', 1, '2024-07-04', NULL, '060277982163', 'no period', 58000000, 0.15),
('STK00079', 1, '2024-07-05', NULL, '060277982164', 'no period', 59000000, 0.15),
('STK00080', 1, '2024-07-05', NULL, '060277982165', 'no period', 60000000, 0.15),
('STK00081', 1, '2024-07-06', NULL, '060277982156', 'no period', 61000000, 0.15),
('STK00082', 1, '2024-07-06', NULL, '060277982156', 'no period', 62000000, 0.15),
('STK00083', 1, '2024-07-07', NULL, '060277982156', 'no period', 63000000, 0.15),
('STK00084', 1, '2024-07-07', NULL, '060277982156', 'no period', 64000000, 0.15),
('STK00085', 1, '2024-07-08', NULL, '060277982156', 'no period', 65000000, 0.15),
('STK00086', 1, '2024-07-08', NULL, '060277982156', 'no period', 66000000, 0.15),
('STK00087', 1, '2024-07-09', NULL, '060277982156', 'no period', 67000000, 0.15),
('STK00088', 1, '2024-07-09', NULL, '060277982156', 'no period', 68000000, 0.15),
('STK00089', 1, '2024-07-10', NULL, '060277982156', 'no period', 69000000, 0.15),
('STK00090', 1, '2024-07-10', NULL, '060277982156', 'no period', 70000000, 0.15);



-- Insert into Tai_khoan_tiet_kiem for July 2024 with 'no period' type starting from STK00091
INSERT INTO Tai_khoan_tiet_kiem (ID_tai_khoan, Trang_thai_tai_khoan, Ngay_mo, Ngay_dong, Nguoi_so_huu, Loai_tiet_kiem, Tien_nap_ban_dau, Lai_suat)
VALUES 
('STK00091', 1, '2024-07-11', NULL, '060277982156', 'no period', 71000000, 0.15),
('STK00092', 1, '2024-07-11', NULL, '060277982156', 'no period', 72000000, 0.15),
('STK00093', 1, '2024-07-11', NULL, '060277982156', 'no period', 73000000, 0.15),
('STK00094', 1, '2024-07-12', NULL, '060277982156', 'no period', 74000000, 0.15),
('STK00095', 1, '2024-07-12', NULL, '060277982156', 'no period', 75000000, 0.15),
('STK00096', 1, '2024-07-12', NULL, '060277982156', 'no period', 76000000, 0.15),
('STK00097', 1, '2024-07-13', NULL, '060277982156', 'no period', 77000000, 0.15),
('STK00098', 1, '2024-07-13', NULL, '060277982156', 'no period', 78000000, 0.15),
('STK00099', 1, '2024-07-13', NULL, '060277982156', 'no period', 79000000, 0.15),
('STK00100', 1, '2024-07-14', NULL, '060277982156', 'no period', 80000000, 0.15),
('STK00101', 1, '2024-07-14', NULL, '060277982156', 'no period', 81000000, 0.15),
('STK00102', 1, '2024-07-14', NULL, '060277982156', 'no period', 82000000, 0.15),
('STK00103', 1, '2024-07-15', NULL, '060277982156', 'no period', 83000000, 0.15),
('STK00104', 1, '2024-07-15', NULL, '060277982156', 'no period', 84000000, 0.15),
('STK00105', 1, '2024-07-15', NULL, '060277982156', 'no period', 85000000, 0.15),
('STK00106', 1, '2024-07-16', NULL, '060277982156', 'no period', 86000000, 0.15),
('STK00107', 1, '2024-07-16', NULL, '060277982156', 'no period', 87000000, 0.15),
('STK00108', 1, '2024-07-16', NULL, '060277982156', 'no period', 88000000, 0.15),
('STK00109', 1, '2024-07-17', NULL, '060277982156', 'no period', 89000000, 0.15),
('STK00110', 1, '2024-07-17', NULL, '060277982156', 'no period', 90000000, 0.15),
('STK00111', 1, '2024-07-17', NULL, '060277982156', 'no period', 91000000, 0.15),
('STK00112', 1, '2024-07-18', NULL, '060277982156', 'no period', 92000000, 0.15),
('STK00113', 1, '2024-07-18', NULL, '060277982156', 'no period', 93000000, 0.15),
('STK00114', 1, '2024-07-18', NULL, '060277982156', 'no period', 94000000, 0.15),
('STK00115', 1, '2024-07-19', NULL, '060277982156', 'no period', 95000000, 0.15),
('STK00116', 1, '2024-07-19', NULL, '060277982156', 'no period', 96000000, 0.15),
('STK00117', 1, '2024-07-19', NULL, '060277982156', 'no period', 97000000, 0.15),
('STK00118', 1, '2024-07-20', NULL, '060277982156', 'no period', 98000000, 0.15),
('STK00119', 1, '2024-07-20', NULL, '060277982156', 'no period', 99000000, 0.15),
('STK00120', 1, '2024-07-20', NULL, '060277982156', 'no period', 100000000, 0.15),
('STK00121', 1, '2024-07-21', NULL, '060277982156', 'no period', 101000000, 0.15),
('STK00122', 1, '2024-07-21', NULL, '060277982156', 'no period', 102000000, 0.15),
('STK00123', 1, '2024-07-21', NULL, '060277982156', 'no period', 103000000, 0.15),
('STK00124', 1, '2024-07-22', NULL, '060277982156', 'no period', 104000000, 0.15),
('STK00125', 1, '2024-07-22', NULL, '060277982156', 'no period', 105000000, 0.15),
('STK00126', 1, '2024-07-22', NULL, '060277982156', 'no period', 106000000, 0.15),
('STK00127', 1, '2024-07-23', NULL, '060277982156', 'no period', 107000000, 0.15),
('STK00128', 1, '2024-07-23', NULL, '060277982156', 'no period', 108000000, 0.15),
('STK00129', 1, '2024-07-23', NULL, '060277982156', 'no period', 109000000, 0.15),
('STK00130', 1, '2024-07-24', NULL, '060277982156', 'no period', 110000000, 0.15),
('STK00131', 1, '2024-07-24', NULL, '060277982156', 'no period', 111000000, 0.15),
('STK00132', 1, '2024-07-24', NULL, '060277982156', 'no period', 112000000, 0.15),
('STK00133', 1, '2024-07-25', NULL, '060277982156', 'no period', 113000000, 0.15),
('STK00134', 1, '2024-07-25', NULL, '060277982156', 'no period', 114000000, 0.15),
('STK00135', 1, '2024-07-25', NULL, '060277982156', 'no period', 115000000, 0.15),
('STK00136', 1, '2024-07-26', NULL, '060277982156', 'no period', 116000000, 0.15),
('STK00137', 1, '2024-07-26', NULL, '060277982156', 'no period', 117000000, 0.15),
('STK00138', 1, '2024-07-26', NULL, '060277982156', 'no period', 118000000, 0.15),
('STK00139', 1, '2024-07-27', NULL, '060277982156', 'no period', 119000000, 0.15),
('STK00140', 1, '2024-07-27', NULL, '060277982156', 'no period', 120000000, 0.15),
('STK00141', 1, '2024-07-27', NULL, '060277982156', 'no period', 121000000, 0.15),
('STK00142', 1, '2024-07-28', NULL, '060277982156', 'no period', 122000000, 0.15),
('STK00143', 1, '2024-07-28', NULL, '060277982156', 'no period', 123000000, 0.15),
('STK00144', 1, '2024-07-28', NULL, '060277982156', 'no period', 124000000, 0.15),
('STK00145', 1, '2024-07-29', NULL, '060277982156', 'no period', 125000000, 0.15),
('STK00146', 1, '2024-07-29', NULL, '060277982156', 'no period', 126000000, 0.15),
('STK00147', 1, '2024-07-29', NULL, '060277982156', 'no period', 127000000, 0.15),
('STK00148', 1, '2024-07-30', NULL, '060277982156', 'no period', 128000000, 0.15),
('STK00149', 1, '2024-07-30', NULL, '060277982156', 'no period', 129000000, 0.15),
('STK00150', 1, '2024-07-30', NULL, '060277982156', 'no period', 130000000, 0.15),
('STK00151', 1, '2024-07-31', NULL, '060277982156', 'no period', 131000000, 0.15),
('STK00152', 1, '2024-07-31', NULL, '060277982156', 'no period', 132000000, 0.15),
('STK00153', 1, '2024-07-31', NULL, '060277982156', 'no period', 133000000, 0.15);



-- Insert into Tai_khoan_tiet_kiem for closed accounts in July 2024
INSERT INTO Tai_khoan_tiet_kiem (ID_tai_khoan, Trang_thai_tai_khoan, Ngay_mo, Ngay_dong, Nguoi_so_huu, Loai_tiet_kiem, Tien_nap_ban_dau, Lai_suat)
VALUES 
('STK00154', 0, '2024-01-01', '2024-07-01', '060277982155', 'no period', 1000000, 0.15),
('STK00155', 0, '2024-01-02', '2024-07-02', '060277982155', 'no period', 2000000, 0.15),
('STK00156', 0, '2024-01-03', '2024-07-03', '060277982155', 'no period', 3000000, 0.15),
('STK00157', 0, '2024-01-04', '2024-07-04', '060277982155', 'no period', 4000000, 0.15),
('STK00158', 0, '2024-01-05', '2024-07-05', '060277982155', 'no period', 5000000, 0.15),
('STK00159', 0, '2024-01-06', '2024-07-06', '060277982155', 'no period', 6000000, 0.15),
('STK00160', 0, '2024-01-07', '2024-07-07', '060277982155', 'no period', 7000000, 0.15),
('STK00161', 0, '2024-01-08', '2024-07-08', '060277982155', 'no period', 8000000, 0.15),
('STK00162', 0, '2024-01-09', '2024-07-09', '060277982155', 'no period', 9000000, 0.15),
('STK00163', 0, '2024-01-10', '2024-07-10', '060277982155', 'no period', 10000000, 0.15),
('STK00164', 0, '2024-01-11', '2024-07-11', '060277982155', 'no period', 11000000, 0.15),
('STK00165', 0, '2024-01-12', '2024-07-12', '060277982155', 'no period', 12000000, 0.15),
('STK00166', 0, '2024-01-13', '2024-07-13', '060277982155', 'no period', 13000000, 0.15),
('STK00167', 0, '2024-01-14', '2024-07-14', '060277982155', 'no period', 14000000, 0.15),
('STK00168', 0, '2024-01-15', '2024-07-15', '060277982155', 'no period', 15000000, 0.15),
('STK00169', 0, '2024-01-16', '2024-07-16', '060277982155', 'no period', 16000000, 0.15),
('STK00170', 0, '2024-01-17', '2024-07-17', '060277982155', 'no period', 17000000, 0.15),
('STK00171', 0, '2024-01-18', '2024-07-18', '060277982155', 'no period', 18000000, 0.15),
('STK00172', 0, '2024-01-19', '2024-07-19', '060277982155', 'no period', 19000000, 0.15),
('STK00173', 0, '2024-01-20', '2024-07-20', '060277982155', 'no period', 20000000, 0.15),
('STK00174', 0, '2024-01-21', '2024-07-21', '060277982155', 'no period', 21000000, 0.15),
('STK00175', 0, '2024-01-22', '2024-07-22', '060277982155', 'no period', 22000000, 0.15),
('STK00176', 0, '2024-01-23', '2024-07-23', '060277982155', 'no period', 23000000, 0.15),
('STK00177', 0, '2024-01-24', '2024-07-24', '060277982155', 'no period', 24000000, 0.15),
('STK00178', 0, '2024-01-25', '2024-07-25', '060277982155', 'no period', 25000000, 0.15),
('STK00179', 0, '2024-01-26', '2024-07-26', '060277982155', 'no period', 26000000, 0.15),
('STK00180', 0, '2024-01-27', '2024-07-27', '060277982155', 'no period', 27000000, 0.15),
('STK00181', 0, '2024-01-28', '2024-07-28', '060277982155', 'no period', 28000000, 0.15),
('STK00182', 0, '2024-01-29', '2024-07-29', '060277982155', 'no period', 29000000, 0.15),
('STK00183', 0, '2024-01-30', '2024-07-30', '060277982155', 'no period', 30000000, 0.15),
('STK00184', 0, '2024-01-31', '2024-07-31', '060277982155', 'no period', 31000000, 0.15),
('STK00185', 0, '2024-02-01', '2024-07-01', '060277982155', 'no period', 32000000, 0.15),
('STK00186', 0, '2024-02-02', '2024-07-02', '060277982155', 'no period', 33000000, 0.15),
('STK00187', 0, '2024-02-03', '2024-07-03', '060277982155', 'no period', 34000000, 0.15),
('STK00188', 0, '2024-02-04', '2024-07-04', '060277982155', 'no period', 35000000, 0.15),
('STK00189', 0, '2024-02-05', '2024-07-05', '060277982155', 'no period', 36000000, 0.15),
('STK00190', 0, '2024-02-06', '2024-07-06', '060277982155', 'no period', 37000000, 0.15),
('STK00191', 0, '2024-02-07', '2024-07-07', '060277982155', 'no period', 38000000, 0.15),
('STK00192', 0, '2024-02-08', '2024-07-08', '060277982155', 'no period', 39000000, 0.15),
('STK00193', 0, '2024-02-09', '2024-07-09', '060277982155', 'no period', 40000000, 0.15),
('STK00194', 0, '2024-02-10', '2024-07-10', '060277982155', 'no period', 41000000, 0.15),
('STK00195', 0, '2024-02-11', '2024-07-11', '060277982155', 'no period', 42000000, 0.15),
('STK00196', 0, '2024-02-12', '2024-07-12', '060277982155', 'no period', 43000000, 0.15),
('STK00197', 0, '2024-02-13', '2024-07-13', '060277982155', 'no period', 44000000, 0.15),
('STK00198', 0, '2024-02-14', '2024-07-14', '060277982155', 'no period', 45000000, 0.15),
('STK00199', 0, '2024-02-15', '2024-07-15', '060277982155', 'no period', 46000000, 0.15),
('STK00200', 0, '2024-02-16', '2024-07-16', '060277982155', 'no period', 47000000, 0.15),
('STK00201', 0, '2024-02-17', '2024-07-17', '060277982155', 'no period', 48000000, 0.15),
('STK00202', 0, '2024-02-18', '2024-07-18', '060277982155', 'no period', 49000000, 0.15),
('STK00203', 0, '2024-02-19', '2024-07-19', '060277982155', 'no period', 50000000, 0.15),
('STK00204', 0, '2024-02-20', '2024-07-20', '060277982155', 'no period', 51000000, 0.15),
('STK00205', 0, '2024-02-21', '2024-07-11', '060277982155', 'no period', 52000000, 0.15),
('STK00206', 0, '2024-02-22', '2024-07-22', '060277982155', 'no period', 53000000, 0.15),
('STK00207', 0, '2024-02-23', '2024-07-23', '060277982155', 'no period', 54000000, 0.15),
('STK00208', 0, '2024-02-24', '2024-07-24', '060277982155', 'no period', 55000000, 0.15),
('STK00209', 0, '2024-02-25', '2024-07-14', '060277982155', 'no period', 56000000, 0.15),
('STK00210', 0, '2024-02-26', '2024-07-13', '060277982155', 'no period', 57000000, 0.15),
('STK00211', 0, '2024-02-27', '2024-07-12', '060277982155', 'no period', 58000000, 0.15),
('STK00212', 0, '2024-02-28', '2024-07-13', '060277982155', 'no period', 59000000, 0.15),
('STK00213', 0, '2024-02-29', '2024-07-14', '060277982155', 'no period', 60000000, 0.15);
INSERT INTO Tai_khoan_tiet_kiem (ID_tai_khoan, Trang_thai_tai_khoan, Ngay_mo, Ngay_dong, Nguoi_so_huu, Loai_tiet_kiem, Tien_nap_ban_dau, Lai_suat)
VALUES 
('STK00214', 0, '2024-02-29', '2024-07-14', '060277982155', 'no period', 60000000, 0.15),
('STK00215', 0, '2024-02-29', '2024-07-14', '060277982155', 'no period', 60000000, 0.15),
('STK00216', 0, '2024-02-29', '2024-07-15', '060277982155', 'no period', 60000000, 0.15);


-- Continue adding for 60 accounts


