document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('.home-button').addEventListener('click', () => {
        window.location.href = '/'
    })
})
$(document).ready(function() {
    function showPage(pageId) {
        $('.page').hide();
        $(`#${pageId}`).show();
    }

    $('#btn-insert-term').click(function() {
        showPage('insert');
    });

    $('#btn-change-minimum-deposit').click(function() {
        showPage('change-minimum-deposit');
    });

    $('#btn-change-minimum-withdraw-day').click(function() {
        showPage('change-minimum-withdraw-day');
    });

    $('#btn-change-interest-rate').click(function() {
        showPage('change-interest-rate');
    });
    $('#btn-display-all-term').click(function() {
        showPage('display-all-term');
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const minimumWithdrawDayInput = document.getElementById('minimum_withdraw_day');
    const minimumDepositMoneyInput = document.getElementById('minimum_deposit');
    const interestRateInput = document.getElementById('interest');

    // Kiểm tra giá trị của minimum_withdraw_day khi người dùng nhập dữ liệu
    minimumWithdrawDayInput.addEventListener('input', () => {
        validateNumberInput(minimumWithdrawDayInput);
    });

    // Kiểm tra giá trị của minimum_deposit_money khi người dùng nhập dữ liệu
    minimumDepositMoneyInput.addEventListener('input', () => {
        validateNumberInput(minimumDepositMoneyInput);
    });

    // Kiểm tra giá trị của interest rate khi người dùng nhập dữ liệu
    interestRateInput.addEventListener('input', () => {
        validateDecimalInput(interestRateInput);
    });

    // Hàm để kiểm tra giá trị chỉ bao gồm số
    function validateNumberInput(inputElement) {
        const value = inputElement.value;

        // Loại bỏ tất cả các ký tự không phải là số
        if (!/^\d*$/.test(value)) {
            inputElement.value = value.replace(/\D/g, '');
        }
    }

    // Hàm để kiểm tra giá trị chỉ bao gồm số và dấu chấm cho số thập phân
    function validateDecimalInput(inputElement) {
        const value = inputElement.value;

        // Loại bỏ tất cả các ký tự không phải là số hoặc dấu chấm
        if (!/^\d*\.?\d*$/.test(value)) {
            inputElement.value = value.replace(/[^0-9.]/g, '');

            // Loại bỏ các dấu chấm thừa (chỉ giữ lại một dấu chấm)
            const parts = inputElement.value.split('.');
            if (parts.length > 2) {
                inputElement.value = parts[0] + '.' + parts.slice(1).join('');
            }
        }
    }
});
