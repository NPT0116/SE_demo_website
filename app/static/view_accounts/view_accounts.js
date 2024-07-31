document.addEventListener('DOMContentLoaded', function() {
    sortOption();
});

function sortOption() {
    var tableHeaders = document.querySelectorAll('th');
    var columnSelect = document.getElementById('column-select');
    columnSelect.innerHTML = '';
    tableHeaders.forEach(function(header, index) {
        var option = document.createElement('option');
        option.textContent = header.textContent.trim();
        option.value = option.textContent;
        columnSelect.appendChild(option);
    });
}

function sortTable() {
    var columnSelect = document.getElementById('column-select');
    var orderSelect = document.getElementById('order-select');
    var column = columnSelect.value;
    var order = orderSelect.value;

    window.location.href = `/view_accounts?sort=${column}&order=${order}`;
}

function resetTable() {
    window.location.href = '/view_accounts';
}

function changeColumnContent() {
    var th = document.getElementById('initial_amount_th');
    var initialAmountCells = document.querySelectorAll('.initial_amount');
    var currentTotalCells = document.querySelectorAll('.current_total');

    if (th.textContent === 'Current Amount') {
        th.textContent = 'Initial Amount';
        initialAmountCells.forEach(function(cell, index) {
            cell.textContent = currentTotalCells[index].dataset.originalContent;
        });
    } else {
        th.textContent = 'Current Amount';
        initialAmountCells.forEach(function(cell, index) {
            if (!currentTotalCells[index].dataset.originalContent) {
                currentTotalCells[index].dataset.originalContent = cell.textContent;
            }
            cell.textContent = currentTotalCells[index].textContent;
        });
    }
    sortOption();
}

function filterTable() {
    var input = document.getElementById('search-input').value.toLowerCase();
    var tableBody = document.getElementById('account-table-body');
    var rows = tableBody.getElementsByTagName('tr');

    for (var i = 0; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        var customerName = cells[2].textContent.toLowerCase();
        var account_ID = cells[1].textContent.toLowerCase();
        if (customerName.includes(input) || account_ID.includes(input)) {
            rows[i].style.display = '';
        } else {
            rows[i].style.display = 'none';
        }
    }
}

function redirectToDetail(accountId) {
    window.location.href = `/view_account_transaction?ID=${accountId}`;
}
document.querySelector('.home-button').addEventListener('click', () => {
    window.location.href = '/'
})