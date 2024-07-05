function updateTime() {
    let now = new Date();

    let hours = now.getHours();
    let minutes = now.getMinutes();
    let period = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12;
    minutes = minutes < 10 ? '0' + minutes : minutes;

    let currentTimeElement = document.getElementById('current-time');
    if (currentTimeElement) {
        currentTimeElement.textContent = `${hours}:${minutes} ${period}`;
    }
}

updateTime();

setInterval(updateTime, 1000);

