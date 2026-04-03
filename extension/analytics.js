document.addEventListener('DOMContentLoaded', () => {
    chrome.storage.local.get(['domainStats'], (res) => {
        const stats = res.domainStats || {};
        renderDashboard(stats);
    });

    document.getElementById('clearDataBtn').addEventListener('click', () => {
        if(confirm("Are you sure you want to clear your analytics data?")) {
            chrome.storage.local.remove('domainStats', () => {
                location.reload();
            });
        }
    });
});

function renderDashboard(stats) {
    const domains = Object.keys(stats);
    if (domains.length === 0) {
        document.getElementById('tableBody').innerHTML = "<tr><td colspan='4' style='text-align:center;'>No data collected yet. Go browse some news!</td></tr>";
        return;
    }

    const formattedStats = domains.map(domain => {
        const total = stats[domain].total;
        const clickbait = stats[domain].clickbait;
        const percentage = total > 0 ? ((clickbait / total) * 100).toFixed(1) : 0;
        return { domain, total, clickbait, percentage };
    }).sort((a, b) => b.percentage - a.percentage);

    const top10 = formattedStats.slice(0, 10);

    const ctx = document.getElementById('clickbaitChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: top10.map(s => s.domain),
            datasets: [{
                label: 'Clickbait %',
                data: top10.map(s => s.percentage),
                backgroundColor: 'rgba(37, 99, 235, 0.7)',
                borderColor: '#2563eb',
                borderWidth: 1,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, max: 100, ticks: { color: '#64748b', font: { weight: 'bold' }, callback: function(value) { return value + "%" } }, grid: { color: '#e2e8f0' } },
                x: { ticks: { color: '#1e293b', font: { weight: 'bold' } }, grid: { display: false } }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });

    const tbody = document.getElementById('tableBody');
    formattedStats.forEach(s => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${s.domain}</td>
            <td>${s.total}</td>
            <td class="text-red">${s.clickbait}</td>
            <td>${s.percentage}%</td>
        `;
        tbody.appendChild(tr);
    });
}
