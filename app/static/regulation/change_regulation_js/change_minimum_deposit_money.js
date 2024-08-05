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


function get_current_money()
{
    var current;

    fetch('/regulation/change_minimum_deposit_money/get_current',
    {
        method: 'GET',
    }
    )
    .then( response => response.json())
    .then( data => {
        current = data['current money'];
        console.log(current);
        return current;

    })
    .catch(error =>
    {
        console.log(error)
        return null;
    }
    )
}
