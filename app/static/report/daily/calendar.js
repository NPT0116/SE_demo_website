document.addEventListener('DOMContentLoaded', function () {
    const daysTag = document.querySelector("#days"),
        currentDate = document.querySelector(".current-date"),
        yearInput = document.querySelector("#year"),
        dateInput = document.querySelector("#ngay");

    let date = new Date(),
        currYear = date.getFullYear(),
        currMonth = date.getMonth();

    const months = ["January", "February", "March", "April", "May", "June", "July",
                    "August", "September", "October", "November", "December"];

    const renderCalendar = () => {
        let firstDayofMonth = new Date(currYear, currMonth, 1).getDay(),
            lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(),
            lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay(),
            lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate();
        let liTag = "";

        for (let i = firstDayofMonth; i > 0; i--) {
            liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
        }

        for (let i = 1; i <= lastDateofMonth; i++) {
            let isToday = i === date.getDate() && currMonth === new Date().getMonth()
                          && currYear === new Date().getFullYear() ? "active" : "";
            liTag += `<li class="${isToday}" data-date="${currYear}-${String(currMonth + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}">${i}</li>`;
        }

        for (let i = lastDayofMonth; i < 6; i++) {
            liTag += `<li class="inactive">${i - lastDayofMonth + 1}</li>`;
        }
        // currentDate.innerText = `${months[currMonth]} ${currYear}`;
        currentDate.innerText = `${months[currMonth]}`;
        daysTag.innerHTML = liTag;

        syncDatePicker();
    }

    const syncDatePicker = () => {
        const selectedDate = dateInput.value;
        if (selectedDate) {
            document.querySelectorAll(".days li").forEach(li => {
                if (li.getAttribute("data-date") === selectedDate) {
                    li.classList.add('selected');
                } else {
                    li.classList.remove('selected');
                }
            });
        }
    }

    daysTag.addEventListener('click', (e) => {
        if (e.target.tagName === 'LI' && !e.target.classList.contains('inactive')) {
            document.querySelectorAll(".days li").forEach(li => li.classList.remove('selected'));
            e.target.classList.add('selected');

            const day = e.target.innerText;
            const selectedDate = `${currYear}-${String(currMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            dateInput.value = selectedDate; // Update the date input field
            console.log('Selected Date:', selectedDate);
        }
    });

    document.querySelector("#prev").addEventListener("click", () => {
        currMonth--;
        if(currMonth < 0) {
            currYear--;
            currMonth = 11;
        }
        renderCalendar();
    });

    document.querySelector("#next").addEventListener("click", () => {
        currMonth++;
        if(currMonth > 11) {
            currYear++;
            currMonth = 0;
        }
        renderCalendar();
    });

    yearInput.addEventListener("input", () => {
        currYear = parseInt(yearInput.value) || new Date().getFullYear();
        renderCalendar();
    });

    renderCalendar();
});
