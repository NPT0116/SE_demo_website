-- Tạo cơ sở dữ liệu QL_TAIKHOANTIETKIEM
DROP DATABASE IF EXISTS QL_TAIKHOANTIETKIEM;

CREATE DATABASE QL_TAIKHOANTIETKIEM;

-- Sử dụng cơ sở dữ liệu QL_TAIKHOANTIETKIEM
USE QL_TAIKHOANTIETKIEM;

-- Tạo bảng Khach_hang
CREATE TABLE Khach_hang (
    ID_khach_hang CHAR(10) NOT NULL,
    Ho_ten NVARCHAR(50) NOT NULL,
    Chung_minh_Thu CHAR(15) NOT NULL,
    Dia_chi NVARCHAR(80) ,
    PRIMARY KEY (ID_khach_hang)
);

-- Tạo bảng Tai_khoan_tiet_kiem
CREATE TABLE Tai_khoan_tiet_kiem (
    ID_tai_khoan CHAR(10) NOT NULL,
    Ngay_mo DATE NOT NULL,
    Nguoi_so_huu CHAR(10) NOT NULL,
    Loai_tiet_kiem NCHAR(20) NOT NULL,
    Tien_nap_ban_dau DECIMAL(19, 4) NOT NULL,
    Lai_suat FLOAT NOT NULL,
    PRIMARY KEY (ID_tai_khoan),
    FOREIGN KEY (Nguoi_so_huu) REFERENCES Khach_hang(ID_khach_hang)
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


-- Thêm các khách hàng vào bảng Khach_hang
INSERT INTO Khach_hang (ID_khach_hang, Ho_ten, Chung_minh_Thu, Dia_chi)
VALUES 
('22127060', 'Lê Hoàng Đạt', '060277982156', '61/21 Liên Khu 1-6, phường Bình Trị Đông, quận Bình Tân'),
('22127088', 'Phạm Quang Duy', '060277982157', '123 Nguyễn Trãi, phường Bến Thành, quận 1'),
('22127298', 'Nguyễn Phúc Thành', '060277982158', '456 Lê Lợi, phường Bến Nghé, quận 1'),
('22127270', 'Nguyễn Quang Minh', '060277982159', '789 Trần Hưng Đạo, phường Cầu Kho, quận 1');


-- Thêm các tài khoản tiết kiệm vào bảng Tai_khoan_tiet_kiem
INSERT INTO Tai_khoan_tiet_kiem (ID_tai_khoan, Ngay_mo, Nguoi_so_huu, Loai_tiet_kiem, Tien_nap_ban_dau, Lai_suat)
VALUES 
('BT001', '2004-04-22', '22127060', '3 Tháng', 100000000, 4.6),
('BT002', '2023-06-15', '22127088', '3 Tháng', 50000000, 2.1),
('ST001', '2023-06-16', '22127298', '6 Tháng', 200000000, 4.6),
('KKH001', '2023-06-17', '22127060', 'Không kỳ hạn', 30000000, 0.15),
('BT003', '2023-06-18', '22127270', '3 Tháng', 70000000, 2.1);

-- Thêm các giao dịch vào bảng Giao_dich
INSERT INTO Giao_dich (ID_giao_dich, Tai_khoan_giao_dich, Loai_giao_dich, So_tien_giao_dich, Ngay_giao_dich)
VALUES 
('RT001', 'KKH001', 'Rút Tiền', 150000000, '2024-06-30'),
('NT001', 'KKH001', 'Nạp Tiền', 430000000, '2024-06-17');

select * from terms;
select * from minimum_withdraw_day;
select * from minimum_deposit_money;
