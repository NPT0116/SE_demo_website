document.addEventListener('DOMContentLoaded', function() {
    // Get references to the table and canvas
    const table = document.querySelector('.table-container');
    const chartCanvas = document.getElementById('myChart');
    const ctx = chartCanvas.getContext('2d');
    const backToTableButton = document.getElementById('backToTableButton');

    // Function to create the chart
    function createChart(labels, revenueData, expenditureData, varianceData) {
        new Chart(ctx, {
            type: 'bar', // Type of chart
            data: {
                labels: labels, // X-axis labels
                datasets: [
                    {
                        label: 'Total Revenue',
                        data: revenueData,
                        backgroundColor: 'rgba(75, 192, 192, 0.5)', // Light color for revenue
                        stack: 'Stack 0', // Grouping in stack
                    },
                    {
                        label: 'Total Expenditure',
                        data: expenditureData,
                        backgroundColor: 'rgba(255, 99, 132, 0.5)', // Light color for expenditure
                        stack: 'Stack 0', // Grouping in stack
                    },
                    {
                        label: 'Variance',
                        data: varianceData,
                        backgroundColor: 'rgba(255, 206, 86, 0.5)', // Light color for variance
                        stack: 'Stack 1', // Different stack for variance
                    }
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
        const revenueData = [];
        const expenditureData = [];
        const varianceData = [];

        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            labels.push(cells[0].textContent); // Label from first cell (e.g., Date)
            const revenue = parseFloat(cells[3].textContent); // Data for total revenue
            const expenditure = parseFloat(cells[4].textContent); // Data for total expenditure
            revenueData.push(revenue);
            expenditureData.push(expenditure);
            varianceData.push(revenue - expenditure); // Calculate variance
        });

        // Hide the table and show the chart
        table.style.display = 'none';
        chartCanvas.style.display = 'block';

        // Create the chart
        createChart(labels, revenueData, expenditureData, varianceData);
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
