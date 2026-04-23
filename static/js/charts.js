function loadCharts(month) {
    let url = '/api/chart-data';
    if (month) url += '?month=' + month;

    fetch(url)
        .then(res => res.json())
        .then(data => {

            if (data.pie.labels.length > 0) {
                new Chart(document.getElementById('pieChart'), {
                    type: 'pie',
                    data: {
                        labels: data.pie.labels,
                        datasets: [{
                            data: data.pie.values,
                            backgroundColor: [
                                '#534ab7','#1D9E75','#EF9F27',
                                '#D85A30','#D4537E','#378ADD',
                                '#639922','#5DCAA5'
                            ],
                            borderWidth: 3,
                            borderColor: '#fff'
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: { font: { size: 12 }, padding: 16 }
                            }
                        }
                    }
                });
            } else {
                document.getElementById('pieChart').parentElement.innerHTML =
                    '<p class="text-muted text-center mt-4">No data yet</p>';
            }

            if (data.bar.labels.length > 0) {
                new Chart(document.getElementById('barChart'), {
                    type: 'bar',
                    data: {
                        labels: data.bar.labels,
                        datasets: [{
                            label: 'Total (₹)',
                            data: data.bar.values,
                            backgroundColor: '#534ab7',
                            borderRadius: 8,
                            borderSkipped: false,
                            barThickness: 40
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: { legend: { display: false } },
                        scales: {
                            y: {
                                beginAtZero: true,
                                grid: { color: '#f0f0f0' },
                                ticks: {
                                    font: { size: 11 },
                                    callback: val => '₹' + val
                                }
                            },
                            x: {
                                grid: { display: false },
                                ticks: { font: { size: 11 } }
                            }
                        }
                    }
                });
            } else {
                document.getElementById('barChart').parentElement.innerHTML =
                    '<p class="text-muted text-center mt-4">No data yet</p>';
            }
        });
}