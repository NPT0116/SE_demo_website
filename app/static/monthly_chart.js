document.addEventListener('DOMContentLoaded', function() {
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(initialize);

    function initialize() {
        document.getElementById('submit').addEventListener('click', function(event) {
            event.preventDefault(); // Ngăn chặn form submit mặc định
            const thang = document.getElementById('thang').value;
            const loai_tiet_kiem = document.getElementById('loai_tiet_kiem').value;
            
            fetch('/report/monthly/get_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ loai_tiet_kiem, thang }),
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                drawChart(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }

    function drawChart(reportData) {
        var dataArray = [['Day', 'Open', 'Close']];
        reportData.forEach(record => {
            dataArray.push([record.ngay.toString(), record.mo_so, record.dong_so]);
        });
        const months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
          ];
          
          let monthNumber = 3; // Ví dụ số tháng là 3 (April)
          let monthName = months[monthNumber - 1]; // Lấy tên tháng từ mảng, trừ 1 vì chỉ số bắt đầu từ 0
          console.log(monthName); // Kết quả là 'April'
          
        var data = google.visualization.arrayToDataTable(dataArray);
        const thang_input = document.getElementById('thang').value;
        const parts = thang_input.split('-');
        const thang =  parseInt(parts[1])
        const nam = parts[0]
        const loai_tiet_kiem = document.getElementById('loai_tiet_kiem').value;

        var options = {
            title: `Number of Savings Books Opened and Closed in ${months[thang-1]} - ${nam} of ${loai_tiet_kiem} term`,
            curveType: 'function',
            legend: { position: 'bottom' },
            hAxis: {
                title: 'Day',
            },
            vAxis: {
                title: 'Count',
                format: '0', // Hiển thị số nguyên thay vì float
            }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
        chart.draw(data, options);
    }
});
