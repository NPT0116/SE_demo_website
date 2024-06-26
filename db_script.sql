DROP DATABASE IF EXISTS saving_account_management;
CREATE DATABASE saving_account_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE saving_account_management;

CREATE TABLE create_account (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ma_so VARCHAR(255) NOT NULL,
    loai_tiet_kiem VARCHAR(255) NOT NULL,
    khach_hang VARCHAR(255) NOT NULL,
    cmnd VARCHAR(255) NOT NULL,
    dia_chi VARCHAR(255) NOT NULL,
    ngay_mo_so DATE NOT NULL,
    so_tien_gui DECIMAL(18, 2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



DESCRIBE create_account;








select * from create_account