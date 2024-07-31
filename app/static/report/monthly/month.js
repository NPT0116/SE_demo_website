const monthList = document.getElementById('monthList');
monthList.innerHTML = '';

const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
];

monthNames.forEach((month, index) => {
    const monthButton = document.createElement('button');
    monthButton.type = 'button';
    monthButton.className = 'month-button';
    monthButton.textContent = month.substring(0,3);
    monthButton.style.backgroundColor = ''
    monthButton.onclick = function() {
        // allDisplayMonth = document.getElementById('monthList')
        const monthList = document.getElementById('monthList')
        const elements = monthList.querySelectorAll('button')
        elements.forEach((e) => {
            e.style.backgroundColor = ''
        })
        monthButton.style.backgroundColor = 'darkgrey'
        document.getElementById('selectedMonth').value = index
    };
    monthList.appendChild(monthButton);
});

document.querySelector('form').addEventListener('submit', function(event) {
    const selectedMonthInput = document.getElementById('selectedMonth');
    if (!selectedMonthInput.value) {
        alert('Please select a month.');
        event.preventDefault(); 
    } 
});
document.querySelector('.home-button').addEventListener('click', () => {
    window.location.href = '/'
})