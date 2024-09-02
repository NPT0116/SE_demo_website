document.addEventListener('DOMContentLoaded', () => {
    // summary information
    const sname = document.querySelector('.s-name');
    const sid = document.querySelector('.s-id');
    const saddress = document.querySelector('.s-address');
    const sopendate = document.querySelector('.s-open-date');
    const sterm = document.querySelector('.s-term');
    const samount = document.querySelector('.s-amount');
    const samount_label = samount.parentElement.querySelector('label')
    document.getElementById('register_account_form').addEventListener('submit', function(event) {
        event.preventDefault(); // Ngăn chặn hành vi gửi form mặc định
    
        // Tạo một đối tượng FormData để thu thập dữ liệu từ form
        var formData = new FormData(this);
    
        // Xóa lớp lỗi và ẩn các thông báo lỗi khỏi tất cả các trường input
        var inputs = document.querySelectorAll('#register_account_form input, #register_account_form select');
        var errorMessages = document.querySelectorAll('.error-message-1, .error-message-2');
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
            var inputs = document.querySelectorAll('#register_account_form input, #register_account_form select');
            inputs.forEach(input => input.classList.remove('error'));
    
            if (data.errors) {
                // Nếu có lỗi, đánh dấu các trường bị lỗi và hiển thị thông báo lỗi
                data.errors.forEach(error => {
                    if (error.includes('name')) {
                        var input = document.getElementById('customer');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('customer_error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    } else if (error.includes('deposit amount')) {
                        var input = document.getElementById('amount');
                        input.classList.add('error');
                        const errorMessage = document.getElementById('amount_error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    } else if (error.includes('term')) {
                        var input = document.getElementById('term');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('term_error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    } else if (error.includes('address')) {
                        var input = document.getElementById('address');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('address_error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    } else if (error.includes('opening date')) {
                        var input = document.getElementById('opening-date');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('opening-date_error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    }
                });
            } else {
                // Nếu không có lỗi, hiển thị thông báo thành công
                alert(data.message);
            }
        })
        .catch(error => {
            // Xử lý lỗi nếu có
            console.error('Error:', error);
            alert('An error occurred while submitting the information');
        });
    });
    // Name check only accept no digit and special char except - and '
    function validateCustomerName(event) {
        const customer = document.getElementById('customer');
        const customerError = document.getElementById('customer_error');
        const parentElement = customer.parentElement;
        const box = parentElement.querySelector('input');
        const label = parentElement.querySelector('label');
        if (event) {
            box.style.border = '2px solid black';
            if (customer.value.trim() !== '' && !/^[\p{L} '-]+$/u.test(customer.value)) {
                customerError.textContent = '*Please input a valid name!';
                box.style.border = '4px solid red';
                label.style.color = 'red';
                sname.textContent = '';
                return false;
            } else if (customer.value.trim() !== '') {
                customerError.textContent = '';
                box.style.border = '4px solid blue';
                label.style.color = 'blue';
                sname.textContent = customer.value.trim();
                return true;
            } else if (customer.value.trim() === '') {
                customerError.textContent = '';
                label.style.color = "black";
                box.style.border = '4px solid black';
                if (event.type === 'blur') {
                    label.style.color = "rgb(99, 102, 102)";
                    box.style.border = '1px solid rgba(0, 0, 0, 0.2)';
                }
                sname.textContent = '';
                return false;
            }
        } else {
            if (/^[\p{L} '-]+$/u.test(customer.value)) {
                return true
            } else {
                return false;
            }
        }
    }
    // id check only accept numeric
    function validateID(event) {
        const id = document.getElementById('ID');
        const idError = document.getElementById('ID_error');
        const parentElement = id.parentElement;
        const box = parentElement.querySelector('input');
        const label = parentElement.querySelector('label')
        if (event) {
            if (id.value.trim() !== '' && !/^\d+$/.test(id.value)) {
                idError.textContent = '*ID must be numeric!';
                box.style.border = '4px solid red';
                label.style.color = 'red'
                sid.textContent = '';
                return false;
            } else if (id.value.trim() !== '') {
                idError.textContent = '';
                box.style.border = '4px solid blue';
                label.style.color = 'blue'
                sid.textContent = id.value.trim();
                return true;
            } else if (id.value.trim() === '') {
                idError.textContent = '';
                label.style.color = "black";
                box.style.border = '4px solid black';
                if (event.type === 'blur') {
                    label.style.color = "rgb(99, 102, 102)";
                    box.style.border = '1px solid rgba(0, 0, 0, 0.2)';
                }
                sid.textContent = '';
                return false;
            }
        } else  {
            if (/^\d+$/.test(id.value)) {
                return true
            } else {
                return false;
            }
        }
    }
    // Address no handle error
    function validateAddress(event) {
        const address = document.getElementById('address');
        const addressError = document.getElementById('address_error');
        const parentElement = address.parentElement;
        const box = parentElement.querySelector('input');
        const label = parentElement.querySelector('label');
        if (event) {
            if (address.value.trim() !== '') {
                box.style.border = '4px solid blue';
                label.style.color = 'blue';
                saddress.textContent = address.value.trim();
                return true;
            } else {
                addressError.textContent = '';
                label.style.color = "black";
                box.style.border = '4px solid black';
                if (event.type === 'blur') {
                    box.style.border = '1px solid rgba(0, 0, 0, 0.2)';
                }
                saddress.textContent = '';
                return false;
            }
        } else {
            if (address.value.trim() !== '') {
                return true;
            } else {
                return false
            }
        }
    }

    // Date no handle Error
    function validateOpeningDate() {
        const openingDate = document.getElementById('opening-date');
        const openingDateError = document.getElementById('opening-date_error');
        const parentElement = openingDate.parentElement;
        const box = parentElement.querySelector('input');
        const label = parentElement.querySelector('label');

        box.style.border = '4px solid blue';
        label.style.color = 'blue'
        return true;
    }

    // Function to validate Term
    function validateTerm(event) {
        const term = document.getElementById('term');
        const termError = document.getElementById('term_error');
        if (event) {
            if (term.value.trim() === 'choose a term' || term.value.trim() === '') {
                sterm.textContent = '';
                return false;
            } else {
                sterm.textContent = term.value.trim();
                return true;
            }
        } else {
            if (term.value.trim() === 'choose a term' || term.value.trim() === '') {
                return false;
            } else {
                return true;
            }
        }
    }
    function formatNumberWithCommas(number) {
        return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    }

    // Remove commas from formatted number
    function removeCommas(number) {
        return number.replace(/,/g, '');
    }

    // Validate and format amount input
    function validateAndFormatAmount(event) {
        const amountInput = document.getElementById('amount');
        const amountError = document.getElementById('amount_error');

        let value = removeCommas(amountInput.value.trim());
        amountInput.value = formatNumberWithCommas(value);
        if (amountInput.value !== '' && !/^\d+$/.test(removeCommas(amountInput.value.trim())) || /^0\d+$/.test(removeCommas(amountInput.value.trim())) || value === '0') {
            samount_label.textContent = '';
            samount.textContent =  '';
            if (/^0\d+$/.test(removeCommas(amountInput.value.trim())) || value === '0') {
                amountError.textContent = '*0 cannot be used to initiate!';
            } else  {
                amountError.textContent = '*Please input numeric amount!';
            }
            amountInput.style.color = 'red'
            return false;
        } else if (/^\d+$/.test(removeCommas(amountInput.value.trim()))) {
            // amountError.textContent = ''
            amountInput.style.color = 'blue'
            samount_label.textContent = 'Initial Balance';
            samount.textContent =  formatNumberWithCommas(value);
            return true;
        }
        //  else if (amountInput.value.trim() === '') {
        //     samount_label.textContent = '';
        //     samount.textContent =  '';
        //     amountError.textContent = '';
        //     return false
        // }
        return false;
    }

    function activateSubmit() {
        const checkName = validateCustomerName();
        const checkID = validateID();
        const checkAddress = validateAddress();
        const checkDate = true;
        const checkAmount = validateAndFormatAmount();
        const checkTerm = validateTerm();

        const submitButton = document.getElementById('submit-button');
        // console.log(checkName, checkID, checkAddress, checkDate, checkAmount, checkTerm)

        const mouseenterHandler = () => {
            submitButton.style.color = "white";
            submitButton.style.backgroundColor = "black";
            submitButton.style.boxShadow = "0 8px 10px gray";
            
        };
        
        const mouseleaveHandler = () => {
            submitButton.style.color = "r#ffffff86";
            submitButton.style.backgroundColor = "#bbbbbb";
            submitButton.style.boxShadow = "0 8px 10px gray";

        };
        const defaultBox = () => {
            submitButton.style.color = "r#ffffff86";
            submitButton.style.backgroundColor = "#bbbbbb";
            submitButton.style.boxShadow = "0 1px 1px rgba(0, 0, 0, 0.367)";
        }
        
        if (checkName && checkID && checkAddress && checkDate && checkAmount && checkTerm) {
            submitButton.style.boxShadow = "0 8px 10px gray";
            submitButton.addEventListener('mouseenter', mouseenterHandler);
            submitButton.addEventListener('mouseleave', mouseleaveHandler);
            submitButton.removeAttribute('disabled');
        } else {
            submitButton.style.color = "r#ffffff86";
            submitButton.style.backgroundColor = "#bbbbbb";
            submitButton.style.boxShadow = "0 1px 1px rgba(0, 0, 0, 0.367)";
            submitButton.addEventListener('mouseenter', defaultBox);
            submitButton.addEventListener('mouseleave', defaultBox);
            submitButton.setAttribute('disabled', 'disabled')
        }
        requestAnimationFrame(activateSubmit);
    }
    activateSubmit()

    // Add event listeners for real-time validation and formatting
    const amountInput = document.getElementById('amount');
    amountInput.addEventListener('input', validateAndFormatAmount);
    amountInput.addEventListener('blur', validateAndFormatAmount);

    // Add event listeners for real-time validation on input change or blur
    document.getElementById('customer').addEventListener('input', validateCustomerName);
    document.getElementById('customer').addEventListener('click', validateCustomerName);
    document.getElementById('customer').addEventListener('blur', validateCustomerName);
    // document.getElementById('customer').addEventListener('input', activateSubmit);

    document.getElementById('ID').addEventListener('input', validateID);
    document.getElementById('ID').addEventListener('click', validateID);
    document.getElementById('ID').addEventListener('blur', validateID);
    // document.getElementById('ID').addEventListener('input', activateSubmit);

    document.getElementById('address').addEventListener('input', validateAddress);
    document.getElementById('address').addEventListener('click', validateAddress);
    document.getElementById('address').addEventListener('blur', validateAddress);
    // document.getElementById('address').addEventListener('input', activateSubmit);

    validateOpeningDate()

    document.getElementById('term').addEventListener('change', validateTerm);
    document.getElementById('term').addEventListener('click', validateTerm);
    document.getElementById('term').addEventListener('blur', validateTerm);
    // document.getElementById('term').addEventListener('change', activateSubmit);

    document.getElementById('amount').addEventListener('input', validateAndFormatAmount);
    document.getElementById('amount').addEventListener('click', validateAndFormatAmount);
    document.getElementById('amount').addEventListener('blur', validateAndFormatAmount);
    // document.getElementById('amount').addEventListener('input', activateSubmit);

    // Submit button
    document.querySelector('.create-account-form').addEventListener('submit', activateSubmit)

    // Home button
    document.querySelector('.home-button').addEventListener('click', () => {
        window.location.href = '/'
    })

    let today = new Date();
    let formattedDate = today.toISOString().split('T')[0];
    document.getElementById('opening-date').value = formattedDate;
    sopendate.textContent = formattedDate;

});



