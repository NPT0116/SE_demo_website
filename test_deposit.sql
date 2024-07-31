USE QL_TAIKHOANTIETKIEM;

INSERT INTO Khach_hang (Ho_ten, Chung_minh_Thu, Dia_chi)
VALUES 
( 'Lỗi nạp vì kì hạn 3 tháng', '1', 'term: 3 tháng'), /*tạo 1 giao dịch nạp vào stk00001*/
( 'Lỗi nạp vì kì hạn 6 tháng', '2', 'term: 6 tháng'), /*tạo 1 giao dịch nạp vào stk00002*/
( 'Lỗi nạp vì ngày trước ngày mở', '3', 'term: 3 tháng'), /*tạo 1 giao dịch nạp vào stk00003 trước ngày 22/4/2024*/
( 'Lỗi nạp vì ngày trước ngày mở', '4', 'term: 6 tháng'), /*tạo 1 giao dịch nạp vào stk00004 trước ngày 15/6/2024*/
( 'Lỗi nạp vì ngày trước ngày mở', '5', 'term: no period'), /*tạo 1 giao dịch nạp vào stk00005 trước ngày 22/4/2024*/
( 'Lỗi nạp vì ngày nạp trong tương lai', '6', 'term: 3 tháng'), /*tạo 1 giao dịch nạp vào stk00006 với ngày nạp là hnay*/
( 'Lỗi nạp vì ngày nạp trong tương lai', '7', 'term: 6 tháng'), /*tạo 1 giao dịch nạp vào stk00007 với ngày nạp là hnay*/
( 'Lỗi nạp vì ngày nạp trong tương lai', '8', 'term: no period'); /*tạo 1 giao dịch nạp vào stk00008 với ngày nạp là hnay*/

INSERT INTO Tai_khoan_tiet_kiem (ID_tai_khoan, Trang_thai_tai_khoan, Ngay_mo, Ngay_dong, Nguoi_so_huu, Loai_tiet_kiem, Tien_nap_ban_dau, Lai_suat)
VALUES 
('STK00001', 1, '2024-04-22', NULL, '1', '3 months', 100000, 0.5),
('STK00002', 1, '2024-06-15', NULL, '2', '6 months', 100000, 0.55),
('STK00003', 1, '2024-04-22', NULL, '3', '3 months', 100000, 0.5),
('STK00004', 1, '2024-06-15', NULL, '4', '6 months', 100000, 0.55),
('STK00005', 1, '2024-04-22', NULL, '5', 'no period', 100000, 0.15),
('STK00006', 1, '2023-06-15', NULL, '6', '6 months', 100000, 0.55),
('STK00007', 1, '2023-04-22', NULL, '7', '3 months', 100000, 0.5),
('STK00008', 1, '2023-06-15', NULL, '8', 'no period', 100000, 0.15),

/*
B1: Chạy sql tạo CSDL
B2: Chạy sql này và tạo các giao dịch nạp tiền ứng với mỗi stk - mỗi stk có tên chủ sở hữu là tên lỗi và địa chỉ là loại kì hạn
*/