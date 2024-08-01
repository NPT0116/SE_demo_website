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
});
