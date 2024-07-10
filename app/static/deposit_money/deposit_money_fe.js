document.addEventListener('DOMContentLoaded', () => {
    let customerName = ''
    let oldBalance = 0
    /*Function to add comma*/
    
   
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
    function removeDot(value) {
        return value.replace(/./g, ''); // Removes all commas from the string
    }
    /* Function to display/remove old balance */
    const oldBalanceBox = document.getElementById('c-old-balance')
    const parent = document.getElementById('card-old-balance')
    const label = parent.querySelector('label')
    function updateOldBalance() {
        if (oldBalance) {
            label.textContent = 'Old Balance'
            oldBalanceBox.textContent = addComma(oldBalance)
        }
        /* Display old balance */
        // document.getElementById('deposit-money').addEventListener('input', logic)
        document.getElementById('deposit-money').addEventListener('input', (event) => {
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
                    fetch('/deposit_money/get_account_info', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: 'ma_so=' + ma_so,
                    })
                    .then(response => response.json())
                    .then(name => {
                        customerName = name['ten_tai_khoan'];
                        return fetch('/deposit_money/get_old_balance', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: 'ma_so=' + ma_so,
                        });
                    })
                    .then(response => response.json())
                    .then(data => {
                        oldBalance = data['Old balance'];
                        console.log(oldBalance);
                        console.log(customerName);
                        updateOldBalance();
                    })
                    .catch(error => {
                        console.error('Error fetching data:', error);
                        customerName = '';
                        oldBalance = 0;
                        removeOldBalance();
                    });
                }
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

        if (customerName !== '') {
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
    // Validate Deposit Date 
    function validateDepositDate(event) {
        const currentDate = takeDate()
        const dateInput = document.getElementById('deposit-date')
        const dateError = document.getElementById('date-error')
        const dateLabel = document.querySelector('label[for="deposit-date"]');
        const c_date = document.getElementById('c-deposit-date')
        const dateValue = dateInput.value.trim()
        if (currentDate !== dateValue) {
            dateError.textContent = '*Deposit date must be current date!'
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
        const amountInput = document.getElementById('deposit-money')
        const amountError = document.getElementById('deposit-money-error')
        const commaValue = amountInput.value.trim()
        const amountValue = removeComma(commaValue)
        console.log(commaValue)
        // Fetch get minimum deposit
        const minimumDeposit = 100
        if (/^\d+$/.test(amountValue) && amountValue >= minimumDeposit) {
            amountError.textContent = ''
            amountInput.style.color = 'blue'
            const formattedInput = addComma(BigInt(amountValue))
            amountInput.value = formattedInput
            console.log(formattedInput)
            console.log(amountInput.value)

            if (amountInput.value === '0') {
                amountInput.value = ''
            }
            return true;
        } else {
            amountInput.style.color = 'red'
            if (amountValue < minimumDeposit) {
                amountError.textContent = '*Amount must be greater than Minimum Amount!'
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
    // ValidateSubmit
    function updateScreen() {
        const id = validateID()
        const name = validateName()
        const date = validateDepositDate()
        const amount = validateAmount()

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
        const oldBalance = document.getElementById('c-old-balance')
        const newBalanceBox = document.getElementById('deposit-money')
        if (id && name && date) {
            document.getElementById('deposit-money').disabled = false;
            console.log(document.getElementById('deposit-money').disabled)
        } else {
            document.getElementById('deposit-money').disabled = true;
            document.getElementById('deposit-money').value = '';
        }
        if (id && name && date && amount) {
            // console.log(oldBalance.textContent)
            const oldBalanceValue = removeComma(oldBalance.textContent)
            const newBalanceValue = removeComma(newBalanceBox.value)

            newBalanceLabel.textContent = 'New Balance'
            newBalance.textContent = addComma(BigInt(oldBalanceValue) + BigInt(newBalanceValue))

            submitButton.style.boxShadow = '0px 0px 10px gray'
            submitButton.style.border = '2px solid black'
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
    document.getElementById('deposit-date').value = formattedDate;
    document.getElementById('deposit-date').style.border = '4px solid green';
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
    document.getElementById('deposit-date').addEventListener('change', validateDepositDate)
    document.getElementById('c-deposit-date').textContent = formattedDate
    // ValidateDepositMoney
    document.getElementById('deposit-money').addEventListener('input', validateAmount)
    // Home Button
    document.querySelector('.home-button').addEventListener('click', () => {
        window.location.href = '/'
    })
    // Submit Button
})