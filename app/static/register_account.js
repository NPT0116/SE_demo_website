document.addEventListener('DOMContentLoaded', function() {
    // Lắng nghe sự kiện 'submit' trên form có id 'myForm'
    document.getElementById('register_account_form').addEventListener('submit', function(event) {
        event.preventDefault(); // Ngăn chặn hành vi gửi form mặc định
        console.alert("i'm here")
        const form = document.getElementById('register_account_form')
        // Tạo một đối tượng FormData để thu thập dữ liệu từ form
        var formData = new FormData(form);
        // Xóa lớp lỗi và ẩn các thông báo lỗi khỏi tất cả các trường input
        var inputs = document.querySelectorAll('#register_account_form input');
        var errorMessages = document.querySelectorAll('.error-message');
        inputs.forEach(input => input.classList.remove('error'));
        errorMessages.forEach(errorMessage => errorMessage.style.display = 'none');

        // Sử dụng Fetch API để gửi dữ liệu đến server
        fetch('/register_account/submit', {
            method: 'POST',
            body: formData // Gửi dữ liệu đã thu thập được
        })
        .then(response => response.json()) // Chuyển đổi phản hồi nhận được thành JSON
        .then(data => {
            // Xóa lớp lỗi khỏi tất cả các trường input
            var inputs = document.querySelectorAll('#register_account_form input');
            inputs.forEach(input => input.classList.remove('error'));

            if (data.errors) {
                // Nếu có lỗi, đánh dấu các trường bị lỗi và hiển thị thông báo lỗi
                data.errors.forEach(error => {
                    if (error.includes('Tên khách hàng')) {
                        var input = document.getElementById('khach_hang');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('khach_hang_error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    } else if (error.includes('CMND')) {
                        var input = document.getElementById('cmnd');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('cmnd_error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    } else if (error.includes('tiền gửi')) {
                        var input = document.getElementById('so_tien_gui');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('so_tien_gui_error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    } else if (error.includes('kỳ hạn')) {
                        var input = document.getElementById('loai_tiet_kiem');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('loai_tiet_kiem_error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    } else if (error.includes('Ngày mở sổ')) {
                        var input = document.getElementById('ngay_mo_so');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('ngay_mo_so_error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    } else if (error.includes('Họ tên khách hàng không khớp')) {
                        var input = document.getElementById('khach_hang');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('khach_hang_error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    } else if (error.includes('Địa chỉ khách hàng không khớp')) {
                        var input = document.getElementById('dia_chi');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('dia_chi_error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    }
                });
                //alert('Có lỗi xảy ra: \n' + data.errors.join('\n'));
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
