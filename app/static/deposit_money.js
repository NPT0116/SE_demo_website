document.addEventListener('DOMContentLoaded', function() {
    // Lắng nghe sự kiện 'submit' trên form có id 'myForm'
    document.getElementById('deposit_money_form').addEventListener('submit', function(event) {
        event.preventDefault(); // Ngăn chặn hành vi gửi form mặc định

        // Tạo một đối tượng FormData để thu thập dữ liệu từ form
        var formData = new FormData(this);

        // Sử dụng Fetch API để gửi dữ liệu đến server
        fetch('/submit_deposit_money', {
            method: 'POST',
            body: formData // Gửi dữ liệu đã thu thập được
        })
        .then(response => response.json()) // Chuyển đổi phản hồi nhận được thành JSON
        .then(data => {
            // Hiển thị thông báo nhận được từ server (cần phía server trả về JSON)
            alert('Thông tin đã được gửi thành công: ' + data.message);
        })
        .catch(error => {
            // Xử lý lỗi nếu có
            console.error('Error:', error);
            alert('Đã xảy ra lỗi khi gửi thông tin');
        });
    });
});
