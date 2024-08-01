function submitForm() {
    var form = document.getElementById('insert_term_form');
    var formData = new FormData(form);
    
    fetch('/regulation/insert_term/submit', {
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
    $(document).ready(function(){
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

});