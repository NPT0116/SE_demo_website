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
    Trang_thai_tai_khoan BOOLEAN NOT NULL,
    Ngay_mo DATE NOT NULL,
    Ngay_dong DATE,
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
('no period', 0.015),
('3 months', 0.05),
('6 months', 0.055);
INSERT INTO minimum_withdraw_day(days) Values
(15);
INSERT INTO minimum_deposit_money( amount) Values
(100000);


INSERT INTO Khach_hang (Ho_ten, Chung_minh_Thu, Dia_chi)
VALUES 
( 'Lê Hoàng Đạt', '060277982156', '61/21 Liên Khu 1-6, phường Bình Trị Đông, quận Bình Tân'),
( 'Phạm Quang Duy', '060277982157', '123 Nguyễn Trãi, phường Bến Thành, quận 1'),
( 'Nguyễn Phúc Thành', '060277982158', '456 Lê Lợi, phường Bến Nghé, quận 1'),
('Nguyễn Quang Minh', '060277982159', '789 Trần Hưng Đạo, phường Cầu Kho, quận 1');


-- Thêm các tài khoản tiết kiệm vào bảng Tai_khoan_tiet_kiem
INSERT INTO Tai_khoan_tiet_kiem (ID_tai_khoan, Trang_thai_tai_khoan, Ngay_mo, Ngay_dong, Nguoi_so_huu, Loai_tiet_kiem, Tien_nap_ban_dau, Lai_suat)
VALUES 
('BT001',1, '2004-04-22',NULL, '060277982156', '3 Tháng', 100000000, 4.6),
('BT002', 1, '2023-06-15', NULL, '060277982157', '3 Tháng', 50000000, 2.1),
('ST001', 1, '2023-06-16', NULL, '060277982158', '6 Tháng', 200000000, 4.6),
('KKH001', 1,'2023-06-17', NULL,'060277982159', 'Không kỳ hạn', 30000000, 0.15),
('BT003', 1, '2023-06-18', NULL,'060277982156', '3 Tháng', 70000000, 2.1);

-- Thêm các giao dịch vào bảng Giao_dich
INSERT INTO Giao_dich (ID_giao_dich, Tai_khoan_giao_dich, Loai_giao_dich, So_tien_giao_dich, Ngay_giao_dich)
VALUES 
('RT001', 'KKH001', 'Rút Tiền', 150000000, '2024-06-30'),
('NT001', 'KKH001', 'Nạp Tiền', 430000000, '2024-06-17');



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



select * from terms;
select * from minimum_withdraw_day;
select * from minimum_deposit_money;

