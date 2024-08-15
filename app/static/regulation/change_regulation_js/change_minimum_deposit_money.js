function submitFormDeposit() {
    var form = document.getElementById('change_minimum_deposit_money_form');
    var formData = new FormData(form);
    event.preventDefault()
    
    fetch('/regulation/change_minimum_deposit_money/submit', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
    // Hiển thị thông báo nhận được từ server (cần phía server trả về JSON)
    alert('Thông tin đã được gửi thành công: ' + data.message);
    })
    .then(data => {
        document.getElementById('result').textContent = data.message;
    })
    .catch(error => {
        document.getElementById('result').textContent = 'Có lỗi xảy ra: ' + error;
    });
}
var formInputs = $('input[type="text"],input[type="number"]');
formInputs.focus(function() {
$(this).parent().children('p.formLabel').addClass('formTop');
$(this).parent().children('span.percentage-sign').addClass('percentage-sign-focus');
$('div.input_container_header').addClass('header-focus')


});
formInputs.focusout(function() {
if ($.trim($(this).val()).length == 0){
$(this).parent().children('p.formLabel').removeClass('formTop');
}
$(this).parent().children('span.percentage-sign').removeClass('percentage-sign-focus');
$('div.input_container_header').removeClass('header-focus')



});
$('p.formLabel').click(function(){
$(this).parent().children('.form-style').focus();

});


async function get_current_money() {
    try {
        const response = await fetch('/regulation/change_minimum_deposit_money/get_current', {
            method: 'GET',
        });

        const data = await response.json();
        return data['current money'];
    } catch (error) {
        console.log('Error fetching current money:', error);
        return null;
    }
}

async function get_current_day() {
    try {
        const response = await fetch('/regulation/change_minimum_withdraw_day/get_current', {
            method: 'GET',
        });

        const data = await response.json();
        const current = data['current day'];
        console.log(current);
        return current;
    } catch (error) {
        console.log('Error fetching current day:', error);
        return null;
    }
}


document.addEventListener('DOMContentLoaded', async () => {
    var current = await get_current_money();
    var current_minimum_deposit = document.getElementsByClassName('current_minimum_deposit');
    
    console.log(current);  // Xem giá trị của current
    
    // Kiểm tra nếu phần tử đầu tiên tồn tại
    if (current_minimum_deposit.length > 0) {
        current_minimum_deposit[0].textContent = current !== null ? current : 'Không thể lấy dữ liệu';
    } else {
        console.log('Không tìm thấy phần tử với class "current_minimum_deposit".');
    }

    console.log(current_minimum_deposit);
    var current = await get_current_day();
    var current_minimum_day = document.getElementsByClassName('current_minimum_day');
    
    console.log(current);  // Xem giá trị của current
    
    // Kiểm tra nếu phần tử đầu tiên tồn tại
    if (current_minimum_day.length > 0) {
        current_minimum_day[0].textContent = current !== null ? current : 'Không thể lấy dữ liệu';
    } else {
        console.log('Không tìm thấy phần tử với class "current_minimum_day".');
    }

    console.log(current_minimum_day);
});
