document.addEventListener('DOMContentLoaded', function() {
    var maSoInput = document.getElementById('ma_so_2');
    var khachHangInput = document.getElementById('khach_hang_2');
    var maSoError = document.getElementById('ma_so_error');

    maSoInput.addEventListener('input', function() {
        var ma_so = maSoInput.value;
        if (ma_so) {
            fetch('/get_account_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'ma_so=' + ma_so,
            })
            .then(response => response.json())
            .then(data => {
                if (data.ten_tai_khoan) {
                    khachHangInput.value = data.ten_tai_khoan;
                    khachHangInput.readOnly = true;
                    maSoError.textContent = ''; // Xóa thông báo lỗi nếu có

                    // Lấy số dư cũ và hiển thị
                    fetch('/get_old_balance', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: 'ma_so=' + ma_so,
                    })
                    .then(response => response.json())
                    .then(balanceData => {
                        if (balanceData['Old balance']) {
                            console.log(`Số dư cũ: ${balanceData['Old balance']}`)
                            document.getElementById('old_balance').textContent = `Số dư cũ: ${balanceData['Old balance']}`;
                        } else {
                            console.log('* Không tìm thấy thông tin tài khoản')
                            document.getElementById('old_balance').textContent = '* Không tìm thấy thông tin tài khoản';
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        document.getElementById('old_balance').textContent = '* Đã xảy ra lỗi khi tìm kiếm số dư cũ';
                    });
                } else {
                    khachHangInput.value = '';
                    khachHangInput.readOnly = false;
                    maSoError.textContent = '* Không tìm thấy thông tin tài khoản';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                maSoError.textContent = '* Đã xảy ra lỗi khi tìm kiếm thông tin tài khoản';
            });
        } else {
            khachHangInput.value = '';
            khachHangInput.readOnly = false;
            maSoError.textContent = '';
        }
    });

    // Lắng nghe sự kiện 'submit' trên form có id 'myForm'
    document.getElementById('deposit_money_form').addEventListener('submit', function(event) {
        event.preventDefault(); // Ngăn chặn hành vi gửi form mặc định

        // Tạo một đối tượng FormData để thu thập dữ liệu từ form
        var formData = new FormData(this);

        // Xóa lớp lỗi và ẩn các thông báo lỗi khỏi tất cả các trường input
        var inputs = document.querySelectorAll('#register_account_form input');
        var errorMessages = document.querySelectorAll('.error-message');
        inputs.forEach(input => input.classList.remove('error'));
        errorMessages.forEach(errorMessage => errorMessage.style.display = 'none');
        
        // Sử dụng Fetch API để gửi dữ liệu đến server
        fetch('/deposit_money/submit', {
            method: 'POST',
            body: formData // Gửi dữ liệu đã thu thập được
        })
        .then(response => response.json()) // Chuyển đổi phản hồi nhận được thành JSON
        .then(data => {
           // Xóa lớp lỗi khỏi tất cả các trường input
           var inputs = document.querySelectorAll('#register_account_form input');
           inputs.forEach(input => input.classList.remove('error'));

           if (data.errors) {
            data.errors.forEach(error => {
                if (error.includes('khách hàng')) {
                    var input = document.getElementById('khach_hang_2');
                    input.classList.add('error');
                    var errorMessage = document.getElementById('khach_hang_error');
                    errorMessage.textContent = '* ' + error;
                    errorMessage.style.display = 'block';
                } else if (error.includes('đóng')) {
                    var input = document.getElementById('ma_so_2');
                    input.classList.add('error');
                    var errorMessage = document.getElementById('ma_so_error');
                    errorMessage.textContent = '* ' + error;
                    errorMessage.style.display = 'block';
                } else if (error.includes('tiền gửi')) {
                    var input = document.getElementById('so_tien_gui_2');
                    input.classList.add('error');
                    var errorMessage = document.getElementById('so_tien_gui_error');
                    errorMessage.textContent = '* ' + error;
                    errorMessage.style.display = 'block';
                } else if (error.includes('Ngày gửi')) {
                    var input = document.getElementById('ngay_goi_2');
                    input.classList.add('error');
                    var errorMessage = document.getElementById('ngay_goi_error');
                    errorMessage.textContent = '* ' + error;
                    errorMessage.style.display = 'block';
                } else if (error.includes('thông tin tài khoản') || error.includes('loại tiết kiệm "no period"')) {
                    var input = document.getElementById('ma_so_2');
                    input.classList.add('error');
                    var errorMessage = document.getElementById('ma_so_error');
                    errorMessage.textContent = '* ' + error;
                    errorMessage.style.display = 'block';
                }
            });
            alert('Có lỗi xảy ra: \n' + data.errors.join('\n'));
            } else {
               // Nếu không có lỗi, hiển thị thông báo thành công
               alert('Thông tin đã được gửi thành công: ' + data.message);
            }
        })
        .catch(error => {
            // Xử lý lỗi nếu có
            console.error('Error:', error);
            alert('Đã xảy ra lỗi khi gửi thông tin');
        });
    });
});
