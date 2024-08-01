
function submitForm() {
    var form = document.getElementById('update_interest_rate_form');
    var hiddenInput = document.getElementById('hidden_interest_period');
    var interestPeriod = document.getElementById('interest_period').textContent;
    hiddenInput.value = interestPeriod
    var formData = new FormData(form);
    event.preventDefault()
    fetch('/regulation/update_interest_rate/submit', {
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
var formInputs = $('input[type="text"],input[type="number"],.selection-box');
formInputs.focus(function() {
$(this).parent().children('p.formLabel').addClass('formTop');
$(this).parent().children('span.percentage-sign').addClass('percentage-sign-focus');
$('div.input_container_header').addClass('header-focus')
$('p.selection-box-label').addClass('selection-box-label-focus');


});
formInputs.focusout(function() {

$(this).parent().children('p.formLabel').removeClass('formTop');

$(this).parent().children('span.percentage-sign').removeClass('percentage-sign-focus');
$('div.input_container_header').removeClass('header-focus')
$('p.selection-box-label').removeClass('selection-box-label-focus');



});
$('p.formLabel').click(function(){
$(this).parent().children('.form-style').focus();

});

});


// Lấy tất cả các phần tử có lớp option-item
const optionBox = document.querySelector('.option-box')
const optionItems = document.querySelectorAll('.option-item');
const outputOption = document.querySelector('.output-option');
const arrow = document.querySelector('.fa-arrow-left');
const selection_box = document.querySelector('.selection-box')
const header = document.querySelector('.input_container_header')
selection_box.addEventListener('click', function()
{

event.stopPropagation();
        if (optionBox.classList.contains('visible')) {
            optionBox.classList.remove('visible');
            arrow.classList.add('fa-arrow-left');
            arrow.classList.remove('fa-arrow-down');
            header.classList.remove('header-focus')
        } else {
            optionBox.classList.add('visible');
            arrow.classList.add('fa-arrow-down');
            arrow.classList.remove('fa-arrow-left');
            header.classList.add('header-focus')

        }

})


document.addEventListener('click', function() {
        arrow.classList.add('fa-arrow-left');
        arrow.classList.remove('fa-arrow-down');
optionBox.classList.remove('visible')

    });
// Thêm sự kiện click cho từng option-item
optionItems.forEach(item => {
    item.addEventListener('click', function() {
        // Xóa lớp selected khỏi tất cả các mục
        optionItems.forEach(i => i.classList.remove('selected'));
        
        // Thêm lớp selected cho mục được chọn
        this.classList.add('selected');

        // Cập nhật nội dung của span output-option
        outputOption.textContent = this.textContent;
    });
});
