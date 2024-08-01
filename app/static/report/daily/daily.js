document.querySelector('form').addEventListener('submit', function(event) {
    const date = document.getElementById('date');
    if (!date.value) {
        alert('Please select a date.');
        event.preventDefault(); 
    } 
    console.log(date.value)
});
document.querySelector('.home-button').addEventListener('click', () => {
    window.location.href = '/'
})

