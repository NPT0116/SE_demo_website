document.addEventListener('DOMContentLoaded', function() {
        // Get references to the table and canvas
        const table = document.querySelector('.table-container');
        const chartCanvas = document.getElementById('myChart');
        const ctx = chartCanvas.getContext('2d');
        const backToTableButton = document.getElementById('backToTableButton');

        // Function to create the chart
        function createChart(labels, openingData, closingData) {
            new Chart(ctx, {
                type: 'bar', // Type of chart
                data: {
                    labels: labels, // X-axis labels
                    datasets: [
                        {
                            label: 'Opening Accounts',
                            data: openingData,
                            backgroundColor: 'rgba(75, 192, 192, 0.5)', // Light color for opening accounts
                            stack: 'Stack 0', // Grouping in stack
                        },
                        {
                            label: 'Closing Accounts',
                            data: closingData,
                            backgroundColor: 'rgba(255, 99, 132, 0.5)', // Light color for closing accounts
                            stack: 'Stack 0', // Grouping in stack
                        },
                        // {
                        //     label: 'Difference',
                        //     data: closingData.map((val, index) => val - openingData[index]),
                        //     backgroundColor: 'rgba(255, 206, 86, 0.5)', // Light color for difference
                        //     stack: 'Stack 1', // Different stack for difference
                        // }
                    ]
                },
                options: {
                    scales: {
                        x: {
                            stacked: true, // Stacking bars on X-axis
                        },
                        y: {
                            stacked: true, // Stacking bars on Y-axis
                            beginAtZero: true // Start Y-axis at zero
                        }
                    }
                }
            });
        }

        // Event handler for table click
        table.addEventListener('click', function() {
            backToTableButton.style.display = 'block';
            // Extract data from the table
            const rows = table.querySelectorAll('tbody tr');
            const labels = [];
            const openingData = [];
            const closingData = [];

            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                labels.push(cells[0].textContent); // Label from first cell
                openingData.push(parseFloat(cells[2].textContent)); // Data for opening accounts
                closingData.push(parseFloat(cells[3].textContent)); // Data for closing accounts
            });

            // Hide the table and show the chart
            table.style.display = 'none';
            chartCanvas.style.display = 'block';

            // Create the chart

            createChart(labels, openingData, closingData);
        });

        // Event handler for "Show Table" button click
        if (backToTableButton) {
            backToTableButton.addEventListener('click', function() {
                chartCanvas.style.display = 'none';
                backToTableButton.style.display = 'none';
                table.style.display = 'block';
            });
        }
    });

