document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('submit').addEventListener('click', function(event) {
        event.preventDefault(); // Ngăn chặn form submit mặc định
        const ngay = document.getElementById('ngay').value;
        
        fetch('/report/daily/get_info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ ngay }),
        })
        .then(response => response.json())
        .then(data => {
            drawChart(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    function drawChart(data) {
        google.charts.load('current', {packages:['corechart', 'bar']});
        google.charts.setOnLoadCallback(function() {
            var dataTable = new google.visualization.DataTable();
            dataTable.addColumn('string', 'Terms');
            dataTable.addColumn('number', 'Deposit');
            dataTable.addColumn({ type: 'string', role: 'annotation' });
            dataTable.addColumn('number', 'Withdraw');
            dataTable.addColumn({ type: 'string', role: 'annotation' });
            dataTable.addColumn('number', 'Difference');
            dataTable.addColumn({ type: 'string', role: 'annotation' });
            data.forEach(function(row) {
                dataTable.addRow([
                    row.loai_tiet_kiem,
                    row.tong_nap, row.tong_nap.toString(),
                    row.tong_rut, row.tong_rut.toString(),
                    row.chenh_lech, row.chenh_lech.toString()
                ]);
            });

            var options = {
                width: 900,
                height: 800,
                legend: { position: 'top', maxLines: 3 },
                bar: { groupWidth: '75%' },
                isStacked: true,
                hAxis: {
                    title: 'Terms'
                },
                vAxis: {
                    title: 'Money(VND)'
                },
                annotations: {
                    alwaysOutside: false, // Chúng ta sẽ để mặc định là false để nó hiển thị bên trong
                    textStyle: {
                        fontSize: 12,
                        auraColor: 'none',
                        color: '#555'
                    },
                    // Thêm các thuộc tính này để thử điều chỉnh vị trí
                    highContrast: true,
                    stem: {
                        length: 16
                    }
                }
            };

            var chart = new google.visualization.ColumnChart(document.getElementById('columnchart_values'));
            chart.draw(dataTable, options);
        });
    }
});
