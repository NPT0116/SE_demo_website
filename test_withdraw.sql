USE QL_TAIKHOANTIETKIEM;

INSERT INTO Khach_hang (Ho_ten, Chung_minh_Thu, Dia_chi)
VALUES 
( 'Lỗi rút vì không đủ số dư', '1', 'term: 3 tháng'),/*tạo giao dịch rút vào tài khoản STK00001 với số tiền > 1*/
( 'Lỗi rút vì không đủ số dư', '2', 'term: 6 tháng'),/*tạo giao dịch rút vào tài khoản STK00002 với số tiền > 1*/
( 'Lỗi rút vì không đủ số dư', '3', 'term: no period'),/*tạo giao dịch rút vào tài khoản STK00003 với số tiền > 1*/
( 'Lỗi rút vì không đủ ngày kỳ hạn (90 ngày)', '4', 'term: 3 tháng'),/*tạo giao dịch rút vào tài khoản STK00004 với ngày rút < 13/10/2024*/
( 'Lỗi rút vì không đủ ngày kỳ hạn (180 ngày)', '5', 'term: 6 tháng'),/*tạo giao dịch rút vào tài khoản STK00005 với ngày rút < 13/1/2025*/
( 'Lỗi rút vì không đủ ngày kỳ hạn (30 ngày)', '6', 'term: no period'),/*tạo giao dịch rút vào tài khoản STK00006 với ngày rút < 13/8/2024*/
( 'Lỗi rút vì không đủ 15 ngày', '7', 'term: 3 tháng'),/*tạo giao dịch rút vào tài khoản STK00007 với ngày rút < 28/7/2024*/
( 'Lỗi rút vì không đủ 15 ngày', '8', 'term: 6 tháng'),/*tạo giao dịch rút vào tài khoản STK00008 với ngày rút < 28/7/2024*/
( 'Lỗi rút vì không đủ 15 ngày', '9', 'term: no period'),/*tạo giao dịch rút vào tài khoản STK00009 với ngày rút < 28/7/2024*/
( 'Lỗi rút vì ngày trước ngày mở', '10', 'term: 3 tháng'),/*tạo giao dịch rút vào tài khoản STK00010 với ngày rút < 21/4/2024*/
( 'Lỗi rút vì ngày trước ngày mở', '11', 'term: 6 tháng'),/*tạo giao dịch rút vào tài khoản STK00011 với ngày rút < 21/4/2024*/
( 'Lỗi rút vì ngày trước ngày mở', '12', 'term: no period'),/*tạo giao dịch rút vào tài khoản STK00012 với ngày rút < 21/4/2024*/
( 'Lỗi rút vì ngày rút trong tương lai', '13', 'term: 3 tháng'),/*tạo giao dịch rút vào tài khoản STK00013 với ngày rút > 2025*/
( 'Lỗi rút vì ngày rút trong tương lai', '14', 'term: 6 tháng'),/*tạo giao dịch rút vào tài khoản STK00014 với ngày rút > 2025*/
( 'Lỗi rút vì ngày rút trong tương lai', '15', 'term: no period');/*tạo giao dịch rút vào tài khoản STK00015 với ngày rút > 2025*/

INSERT INTO Tai_khoan_tiet_kiem (ID_tai_khoan, Trang_thai_tai_khoan, Ngay_mo, Ngay_dong, Nguoi_so_huu, Loai_tiet_kiem, Tien_nap_ban_dau, Lai_suat)
VALUES 
('STK00001', 1, '2024-04-22', NULL, '1', '3 months', 1, 0.5),
('STK00002', 1, '2024-06-15', NULL, '2', '6 months', 1, 0.55),
('STK00003', 1, '2024-04-22', NULL, '3', 'no period', 1, 0.15),
('STK00004', 1, '2024-07-13', NULL, '4', '3 months', 100000, 0.5),
('STK00005', 1, '2024-07-13', NULL, '5', '6 months', 100000, 0.55),
('STK00006', 1, '2024-07-13', NULL, '6', 'no period', 100000, 0.15),
('STK00007', 1, '2024-07-13', NULL, '7', '3 months', 100000, 0.5),
('STK00008', 1, '2024-07-13', NULL, '8', '6 months', 100000, 0.55),
('STK00009', 1, '2024-07-13', NULL, '9', 'no period', 100000, 0.15),
('STK00010', 1, '2025-04-22', NULL, '10', '3 months', 100000, 0.5),
('STK00011', 1, '2025-04-22', NULL, '11', '6 months', 100000, 0.55),
('STK00012', 1, '2025-04-22', NULL, '12', 'no period', 100000, 0.15),
('STK00013', 1, '2023-04-22', NULL, '13', '3 months', 100000, 0.5),
('STK00014', 1, '2023-06-15', NULL, '14', '6 months', 100000, 0.55),
('STK00015', 1, '2023-04-22', NULL, '15', 'no period', 100000, 0.15),

/*
B1: Chạy sql tạo CSDL
B2: Chạy sql này và tạo các giao dịch rút tiền ứng với mỗi stk - mỗi stk có tên chủ sở hữu là tên lỗi và địa chỉ là loại kì hạn
*/