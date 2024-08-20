document.addEventListener('DOMContentLoaded', () => {
    let customerName = '';
    let oldBalance = 0;
    let account_status ;
    let term ;
    let initial_money;
    let interest ;
    let interest_money = 0;
    var old_balance = 0;
    /*Function to add comma*/
    const form = document.querySelector('#withdraw_money_form')
    // Submit Button
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Ngăn chặn hành vi gửi form mặc định

        // Tạo một đối tượng FormData để thu thập dữ liệu từ form
        var formData = new FormData(this);

        // Xóa lớp lỗi và ẩn các thông báo lỗi khỏi tất cả các trường input
        var inputs = document.querySelectorAll('#withdraw_money_form input');
        var errorMessages = document.querySelectorAll('.error-message');
        inputs.forEach(input => input.classList.remove('error'));
        errorMessages.forEach(errorMessage => errorMessage.style.display = 'none');
        
        // Sử dụng Fetch API để gửi dữ liệu đến server
        fetch('/withdraw_money/submit', {
            method: 'POST',
            body: formData // Gửi dữ liệu đã thu thập được
        })
        .then(response => response.json()) // Chuyển đổi phản hồi nhận được thành JSON
        .then(data => {
            // Xóa lớp lỗi khỏi tất cả các trường input
            inputs.forEach(input => input.classList.remove('error'));

            if (data.errors) {
                data.errors.forEach(error => {
                    if (error.includes('Số tiền rút') || error.includes('rút hết toàn bộ')) {
                        var input = document.getElementById('withdraw-money');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('withdraw-money-error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    } else if (error.includes('Ngày rút') || error.includes('giao dịch gần nhất') || error.includes('thời gian tối thiểu')) {
                        var input = document.getElementById('withdraw-date');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('date-error');
                        errorMessage.textContent = '* ' + error;
                        errorMessage.style.display = 'block';
                    } else if (error.includes('Mã số') || error.includes('thông tin tài khoản') || error.includes('đóng')) {
                        var input = document.getElementById('id');
                        input.classList.add('error');
                        var errorMessage = document.getElementById('id-error');
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
    function addComma(value) {
        if (typeof value !== 'bigint' && typeof value !== 'number') {
            return ''
        }
        let formattedValue = typeof value === 'bigint' ? value.toString() : value.toLocaleString('en')
        return formattedValue.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    }
    /* Function to remove comma and parse as BigInt */
    function removeComma(value) {
        return value.replace(/[,\.]/g, ''); // Removes all commas and dots from the string
    }
    /* Function to display/remove old balance */
    const oldBalanceBox = document.getElementById('c-old-balance')
    const parent = document.getElementById('card-old-balance')
    const label = parent.querySelector('label')
    function updateOldBalance() {
        // console.log(oldBalance)
        if (oldBalance) {
            label.textContent = 'Old Balance'
            oldBalanceBox.textContent = addComma(parseInt(oldBalance))
        } else {
            label.textContent = ''
            oldBalanceBox.textContent = ''
        }
        /* Display old balance */
        document.getElementById('withdraw-money').addEventListener('input', (event) => {
            let value = event.target.value.replace(/\D/g, '')
            if (value) {
                event.target.value = new Intl.NumberFormat().format(value)
            }
        })
    }
    function removeOldBalance() {
        label.textContent = ''
        oldBalanceBox.textContent = ''
    }
    /* Take date */
    function takeDate() {
        const currentDate = new Date();
        const year = currentDate.getFullYear();
        const month = String(currentDate.getMonth() + 1).padStart(2, '0')
        const day = String(currentDate.getDate()).padStart(2, '0')
        const date = `${year}-${month}-${day}`
        return date
    }
    /* Validate function */
    // Validate input ID
    function validateID(event) {
        const idInput = document.getElementById('id')
        const idError = document.getElementById('id-error')
        const idLabel = document.querySelector(`label[for="id"]`)
        const c_id = document.getElementById('c-id')
        const idValue = idInput.value.trim()
        var ma_so = idValue
        if (event) {
            if (/^[a-zA-Z]+\d+$/.test(idValue)) {
                idError.textContent = ''
                idLabel.style.color = 'green'
                idInput.style.border = '4px solid green'
                c_id.textContent = idValue
                // Fetch Name cho nay nha Duy gan do customerName
                if (idValue) {
                    fetch('/withdraw_money/get_account_info', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: 'ma_so=' + ma_so,
                    })
                    .then(response => response.json())
                    .then(name => {
                        // console.log(typeof name)
                        customerName = name['ten_tai_khoan'];
                        account_status = name['Trang_thai_tai_khoan']
                        term = name['loai_tiet_kiem']
                        initial_money = name['Tien_nap_ban_dau']
                        interest = name['Lai_suat']
                        old_balance = name['old_balance']
                        // console.log(customerName)
                        // console.log(account_status)
                        // console.log(initial_money)
                        // console.log(interest)

                        if (term == "no period" || term == "Không kỳ hạn")
                        {                            
                            fetch('/deposit_money/get_old_balance', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/x-www-form-urlencoded',
                                },
                                body: 'ma_so=' + ma_so,
                            })
                            .then(response => response.json())
                            .then(data => {
                                // oldBalance = data['Old balance'];
                                oldBalance = old_balance
                                updateOldBalance();
                            }) 
                        }
                        else
                        {
                            oldBalance = initial_money
                            fetch('/withdraw_money/get_interest_money', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/x-www-form-urlencoded',
                                },
                                body: 'ma_so=' + ma_so,
                            })
                            .then(response => response.json())
                            .then(data => {
                                interest_money = data['Interest_money'];
                                updateOldBalance();
                            }) 
                        }
                        // console.log(oldBalance)
                        // console.log(interest_money)
                    })
                    .catch(error => {
                        console.error('Error fetching data:', error);
                        customerName = '';
                        oldBalance = 0;
                        removeOldBalance();
                    });
                }
                // Fetch Old Balance cho nay
                updateOldBalance()
                return true;
            } else if (idValue !== '') {
                customerName = ''
                idLabel.style.color = 'red'
                idInput.style.border = '4px solid red'
                idError.textContent = '*ID must contain letters followed by numbers!'
                c_id.textContent = ''
                removeOldBalance()
                return false;
            } else {
                customerName = ''
                idError.textContent = ''
                idLabel.style.color = 'black'
                idInput.style.border = '4px solid black'
                c_id.textContent = ''
                if (event.type === 'blur') {
                    idInput.style.border = ''
                    idLabel.style.color = 'rgb(99, 102, 102)'
                }
                removeOldBalance()
                return false;
            }
        } else {
            if (/^[a-zA-Z]+\d+$/.test(idValue)) {
                return true;
            } else {
                return false;
            }
        }
    }
    // Validate Name
    function validateName(event) {
        const nameInput = document.getElementById('name')
        const nameLabel = document.querySelector(`label[for="name"]`)
        const nameError = document.getElementById('name-error')
        const c_name = document.getElementById('c-name')
        const nameValue = customerName

        if (customerName !== '' && customerName) {
            c_name.textContent = nameValue
            nameInput.value = nameValue
            nameInput.style.border = '4px solid green'
            nameLabel.style.color = 'green'
            return true;
        } else {
            c_name.textContent = nameValue
            nameInput.value = nameValue
            nameInput.style.border = '1px solid rgba(0, 0, 0, 0.2)'
            nameLabel.style.color = 'rgb(99, 102, 102)'
            return false;
        }
    }
    // Validate Withdraw Date 
    function validateWithdrawDate(event) {
        const currentDate = takeDate()
        const dateInput = document.getElementById('withdraw-date')
        const dateError = document.getElementById('date-error')
        const dateLabel = document.querySelector('label[for="withdraw-date"]');
        const c_date = document.getElementById('c-withdraw-date')
        const dateValue = dateInput.value.trim()
        if (currentDate !== dateValue) {
            dateError.textContent = '*Withdraw date must be current date!'
            dateLabel.style.color = 'red'
            dateInput.style.border = '4px solid red'
            c_date.textContent = ''
            return false;
        } else {
            dateError.textContent = ''
            dateLabel.style.color = 'green'
            dateInput.style.border = '4px solid green'
            c_date.textContent = dateValue
            return true;
        }
    }
    // Validate Amount
    function isFormattedNumber(value) {
        const formattedNumberPattern = /^(\d{1,3}(,\d{3})*|\d+)$/;
        return formattedNumberPattern.test(value);
    }
    function validateAmount(event) {
        const amountInput = document.getElementById('withdraw-money')
        const amountError = document.getElementById('withdraw-money-error')
        const commaValue = amountInput.value.trim()
        const amountValue = removeComma(commaValue)

        const maxWithdraw = oldBalance
        if (term) {
            if (term != 'no period' && term != 'Không kỳ hạn') {
                return true;
            }
    
            if (/^\d+$/.test(amountValue) && parseInt(amountValue) <= parseInt(maxWithdraw)) {
                amountError.textContent = ''
                amountInput.style.color = 'blue'
                const formattedInput = addComma(BigInt(amountValue))
                amountInput.value = formattedInput
                if (amountInput.value === '0') {
                    amountInput.value = ''
                }
                return true;
            } else {
                amountInput.style.color = 'red'
                if (parseInt(amountValue) > parseInt(maxWithdraw)) {
                    amountError.textContent = '*Amount must be smaller than Current Balance!'
                } else {
                    amountError.textContent = '*Value must be numeric!'
                }
                if (amountValue === '') {
                    amountInput.style.color = 'blue'
                    amountError.textContent = ''
                }
                return false;
            }
        }
    }
    // ValidateSubmit
    function updateScreen() {
        const id = validateID()
        const name = validateName()
        const date = validateWithdrawDate()
        const amount = validateAmount()
        let inputBox = document.getElementById('withdraw-money')
        let displayTerm = document.getElementById("c-term")
        let parentOfAmountBox = inputBox.parentElement

        if (term) {
            displayTerm.textContent = term
            if (term != 'no period' && term != 'Không kỳ hạn') {
                inputBox.disabled = false;
                inputBox.value = addComma(parseInt(oldBalance))
                parentOfAmountBox.style.opacity = 0.5;
            }                       
        }  else {
            displayTerm.textContent = ''
            inputBox.value = ''
            inputBox.disabled = false;  
            parentOfAmountBox.style.opacity = 1; 
        }

        const submitButton = document.getElementById('submit-button')
        const handleMouseEnter = () => {
            // customerName = 'DUY'
            submitButton.style.boxShadow = '0px 0px 10px gray'
            submitButton.style.border = '20px solid white'
            submitButton.style.backgroundColor = 'black'
            submitButton.style.color = 'white'
        }
        const handleMouseLeave = () => {
            submitButton.style.boxShadow = '0px 0px 10px gray'
            submitButton.style.border = '2px solid black'
            submitButton.style.backgroundColor = ''
            // submitButton.style.color = 'black'
        }
        const handleSpecialLeave = () => {
            submitButton.style.backgroundColor = ''
            submitButton.style.border = ''
            submitButton.style.color = 'white'
        }
        const newBalance = document.getElementById('c-new-balance')
        const newBalanceLabel = document.querySelector('label[for="c-new-balance"]')
        const oldBalanceBox = document.getElementById('c-old-balance')
        const newBalanceBox = document.getElementById('withdraw-money')

        if (id && name && date && amount) {
            // const oldBalanceValue = removeComma(oldBalanceBox.textContent)
            // const newBalanceValue = removeComma(newBalanceBox.value)
            const oldBalanceValue = removeComma(oldBalanceBox.textContent)
            // const newBalanceValue = removeComma(newBalanceBox.value)

            if (term) {
                if (term != 'no period' && term != 'Không kỳ hạn') {
                    newBalanceLabel.textContent = 'Interest Money'
                    newBalance.textContent = addComma(interest_money)
                } else {
                    newBalanceLabel.textContent = 'New Balance'
                    const amountInput = document.getElementById('withdraw-money')
                    // console.log(amountInput.value)
                    const new_money = oldBalanceValue - removeComma(amountInput.value)
                    newBalance.textContent = addComma(new_money)
                }
            }

            submitButton.style.boxShadow = '0px 0px 10px gray'
            submitButton.style.border = '2px solid black'
            submitButton.disabled = false;
            // submitButton.style.color = 'black'
            if (!submitButton.hasMouseEnterListener) {
                submitButton.addEventListener('mouseenter', handleMouseEnter);
                submitButton.addEventListener('mouseleave', handleMouseLeave);
                submitButton.hasMouseEnterListener = true;
            }
        } else {
            newBalance.textContent = ''
            newBalanceLabel.textContent = ''
            submitButton.style.boxShadow = ''
            submitButton.style.border = ''
            submitButton.style.color = 'white'
            submitButton.disabled = true;
            if (submitButton.hasMouseEnterListener) {
                submitButton.addEventListener('mouseenter', handleSpecialLeave);
                submitButton.removeEventListener('mouseenter', handleMouseEnter);
                submitButton.removeEventListener('mouseleave', handleMouseLeave);
                submitButton.hasMouseEnterListener = false;
            }
        }
        requestAnimationFrame(updateScreen)
    }
    updateScreen()
    /* Set current Date */
    let today = new Date();
    let formattedDate = today.toISOString().split('T')[0];

    document.getElementById('withdraw-date').value = formattedDate;
    document.getElementById('withdraw-date').style.border = '4px solid green';
    /* Add Listener and Animation */
    // ValidateID
    document.getElementById('id').addEventListener('input', validateID)
    document.getElementById('id').addEventListener('click', validateID)
    document.getElementById('id').addEventListener('blur', validateID)
    // ValidateName
    document.getElementById('name').addEventListener('input', validateName)
    document.getElementById('name').addEventListener('click', validateName)
    document.getElementById('name').addEventListener('blur', validateName)
    // ValidateDate
    document.getElementById('withdraw-date').addEventListener('change', validateWithdrawDate)
    document.getElementById('c-withdraw-date').textContent = formattedDate
    // ValidateWithdrawMoney
    document.getElementById('withdraw-money').addEventListener('input', validateAmount)
    // Home Button
    document.querySelector('.home-button').addEventListener('click', () => {
        window.location.href = '/'
    })
})