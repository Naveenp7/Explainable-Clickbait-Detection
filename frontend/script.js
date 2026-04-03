const API_URL = "http://localhost:8000";

const elements = {
    input: document.getElementById('headlineInput'),
    btn: document.getElementById('analyzeBtn'),
    btnText: document.querySelector('.btn-text'),
    loader: document.querySelector('.loader'),
    results: document.getElementById('resultsSection'),
    errorSection: document.getElementById('errorSection'),
    errorMessage: document.getElementById('errorMessage'),
    badge: document.getElementById('resultBadge'),
    highlightedText: document.getElementById('highlightedText'),
    confidenceChart: document.getElementById('confidenceChart'),
    limeChart: document.getElementById('limeChart')
};

let confChartInstance = null;
let limeChartInstance = null;

elements.btn.addEventListener('click', analyzeHeadline);
elements.input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        analyzeHeadline();
    }
});

async function analyzeHeadline() {
    const headline = elements.input.value.trim();
    if (!headline) return;

    setLoading(true);
    hideError();
    elements.results.classList.add('hidden');

    try {
        // 1. Predict
        const predRes = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ headlines: [headline] })
        });
        if(!predRes.ok) throw new Error("Prediction API Error");
        const predData = await predRes.json();
        const prediction = predData.predictions[0];

        // 2. Explain
        const expRes = await fetch(`${API_URL}/explain`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ headline: headline })
        });
        if(!expRes.ok) throw new Error("Explanation API Error");
        const expData = await expRes.json();
        const explanation = expData.explanation;

        displayResults(headline, prediction, explanation);
    } catch (err) {
        showError("Failed to connect to the analysis engine. Ensure backend is running. " + err.message);
    } finally {
        setLoading(false);
    }
}

function setLoading(isLoading) {
    if (isLoading) {
        elements.btn.disabled = true;
        elements.btnText.textContent = "Analyzing...";
        elements.loader.classList.remove('hidden');
    } else {
        elements.btn.disabled = false;
        elements.btnText.textContent = "Analyze Headline";
        elements.loader.classList.add('hidden');
    }
}

function displayResults(headline, prediction, explanation) {
    elements.results.classList.remove('hidden');

    // Badge
    if (prediction.is_clickbait) {
        elements.badge.textContent = "Clickbait Detected";
        elements.badge.className = "result-badge badge-danger";
    } else {
        elements.badge.textContent = "Looks Safe";
        elements.badge.className = "result-badge badge-success";
    }

    // Confidence Chart
    renderConfidenceChart(prediction.probabilities);

    // LIME Highlighted Text
    renderHighlights(headline, explanation);

    // LIME Bar Chart
    renderLimeChart(explanation);
}

function renderHighlights(text, explanation) {
    let wordScores = {};
    let maxAbsScore = 0;
    
    explanation.forEach(([word, score]) => {
        const cleanWord = word.replace(/[^\w\s]/g, '').toLowerCase();
        wordScores[cleanWord] = score;
        if (Math.abs(score) > maxAbsScore) maxAbsScore = Math.abs(score);
    });

    const tokens = text.split(/(\s+|[.,!?;'"])/);
    
    let html = "";
    tokens.forEach(token => {
        const cleanToken = token.replace(/[^\w\s]/gi, '').toLowerCase();
        const score = wordScores[cleanToken];

        if (score !== undefined && score !== 0) {
            const intensity = Math.min(Math.abs(score) / (maxAbsScore || 1) + 0.1, 1);
            const isClickbaitWeight = score > 0;
            const color = isClickbaitWeight ? `rgba(239, 68, 68, ${intensity})` : `rgba(16, 185, 129, ${intensity})`;
            
            html += `<span class="highlight-word" style="background-color: ${color};" title="Weight: ${score.toFixed(4)}">${token}</span>`;
        } else {
            html += token;
        }
    });

    elements.highlightedText.innerHTML = html;
}

function renderConfidenceChart(probs) {
    if (confChartInstance) confChartInstance.destroy();
    
    const ctx = elements.confidenceChart.getContext('2d');
    
    confChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Non-Clickbait', 'Clickbait'],
            datasets: [{
                data: [probs[0] * 100, probs[1] * 100],
                backgroundColor: ['#10b981', '#ef4444'],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: { position: 'bottom', labels: { color: '#475569' } }
            }
        }
    });
}

function renderLimeChart(explanation) {
    if (limeChartInstance) limeChartInstance.destroy();
    
    const ctx = elements.limeChart.getContext('2d');
    
    const labels = explanation.map(e => e[0]);
    const data = explanation.map(e => e[1]);
    const bgColors = data.map(val => val > 0 ? 'rgba(239, 68, 68, 0.8)' : 'rgba(16, 185, 129, 0.8)');

    limeChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Word Impact (LIME)',
                data: data,
                backgroundColor: bgColors,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(0,0,0,0.05)' },
                    ticks: { color: '#64748b' }
                },
                y: {
                    grid: { display: false },
                    ticks: { color: '#1e293b' }
                }
            }
        }
    });
}

function showError(msg) {
    elements.errorMessage.textContent = msg;
    elements.errorSection.classList.remove('hidden');
}

function hideError() {
    elements.errorSection.classList.add('hidden');
}
