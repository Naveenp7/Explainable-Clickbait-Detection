let isEnabled = true;
let isBlurEnabled = false;

chrome.storage.local.get(['extensionEnabled', 'blurEnabled'], (res) => {
    if (res.extensionEnabled !== undefined) isEnabled = res.extensionEnabled;
    if (res.blurEnabled !== undefined) isBlurEnabled = res.blurEnabled;
    if (isEnabled) scanHeadlines();
});

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
    if (msg.action === "toggle") {
        isEnabled = msg.state;
        if (isEnabled) {
            scanHeadlines();
        } else {
            removeHighlights();
        }
    }
    if (msg.action === "blurToggle") {
        isBlurEnabled = msg.state;
        if (isEnabled) scanHeadlines(); // re-scan to apply or remove blur
    }
});

async function scanHeadlines() {
    // Check for standard headings and link elements usually used for news articles
    const headings = document.querySelectorAll('h1, h2, h3, h4, article a, [role="heading"] a, a[class*="title"], a[class*="heading"]');
    const batch = [];
    const elements = [];

    headings.forEach(heading => {
        const text = heading.innerText.trim();
        if (text.split(' ').length > 3 && !heading.dataset.cbProcessed) {
            batch.push(text);
            elements.push(heading);
            heading.dataset.cbProcessed = "true";
        }
    });

    if (batch.length === 0) return;

    for (let i = 0; i < batch.length; i += 20) {
        const textBatch = batch.slice(i, i + 20);
        const elemBatch = elements.slice(i, i + 20);

        try {
            chrome.runtime.sendMessage({ type: "PREDICT", headlines: textBatch }, (response) => {
                if (!response || !response.success) return;
                const data = response.data;
                let cbCount = 0;
                data.predictions.forEach((pred, idx) => {
                    if (pred.is_clickbait) {
                        cbCount++;
                        highlightElement(elemBatch[idx], pred.confidence);
                    } else {
                        markSafeElement(elemBatch[idx]);
                    }
                });

                // Save domain statistics
                chrome.storage.local.get(['domainStats'], (statsRes) => {
                    const stats = statsRes.domainStats || {};
                    const domain = window.location.hostname;
                    if (!stats[domain]) stats[domain] = { total: 0, clickbait: 0 };
                    stats[domain].total += data.predictions.length;
                    stats[domain].clickbait += cbCount;
                    chrome.storage.local.set({ domainStats: stats });
                });
            });
        } catch (e) {
            console.error("Clickbait API error:", e);
        }
    }
}

function highlightElement(el, confidence) {
    el.classList.add('cb-detected');
    if (isBlurEnabled) {
        el.classList.add('cb-blurred');
    } else {
        el.classList.remove('cb-blurred');
    }
    el.style.borderLeft = "4px solid #ef4444";
    el.style.paddingLeft = "8px";
    el.title = `Clickbait Detected (${(confidence * 100).toFixed(1)}% confidence). Hover for explanation.`;

    let tooltipTimeout;
    el.addEventListener('mouseenter', (e) => {
        tooltipTimeout = setTimeout(() => showTooltip(el), 800);
    });
    
    el.addEventListener('mouseleave', () => {
        clearTimeout(tooltipTimeout);
        hideTooltip();
    });
}

function markSafeElement(el) {
    el.classList.add('cb-safe');
    el.classList.remove('cb-blurred');
    el.style.borderLeft = "4px solid #10b981";
    el.style.paddingLeft = "8px";
    el.title = `Looks Safe. Hover for AI explanation.`;

    let tooltipTimeout;
    el.addEventListener('mouseenter', (e) => {
        tooltipTimeout = setTimeout(() => showTooltip(el), 800);
    });
    
    el.addEventListener('mouseleave', () => {
        clearTimeout(tooltipTimeout);
        hideTooltip();
    });
}

function removeHighlights() {
    document.querySelectorAll('.cb-detected, .cb-safe').forEach(el => {
        el.classList.remove('cb-detected', 'cb-safe', 'cb-blurred');
        el.style.borderLeft = "";
        el.style.paddingLeft = "";
        el.title = "";
    });
}

const tooltip = document.createElement('div');
tooltip.id = 'cb-tooltip';
document.body.appendChild(tooltip);

async function showTooltip(el) {
    const text = el.innerText.trim();
    const rect = el.getBoundingClientRect();
    
    tooltip.innerHTML = "<div class='cb-loader'>Loading explanation...</div>";
    tooltip.style.top = `${window.scrollY + rect.top - window.innerHeight * 0.15}px`;
    tooltip.style.left = `${rect.left}px`;
    tooltip.classList.add('cb-visible');

    try {
        chrome.runtime.sendMessage({ type: "EXPLAIN", headline: text }, (response) => {
            if (!response || !response.success) {
                tooltip.innerHTML = `<div class='cb-error'>Error: Ensure backend API is running.</div>`;
                return;
            }
            
            // Re-fetch category status for the specific hovered headline features
            const isClickbait = el.classList.contains('cb-detected');
            const confidenceStr = el.title.match(/(\d+\.\d+)%/);
            const confidence = confidenceStr ? parseFloat(confidenceStr[1]) / 100 : 0.5;

            renderLIME(response.data.explanation, text, isClickbait, confidence);
        });
    } catch (e) {
        tooltip.innerHTML = `<div class='cb-error'>Error: Ensure backend API is running.</div>`;
    }
}

function renderLIME(explanation, text, isClickbait, confidence) {
    const tooltip = document.getElementById('cb-tooltip');
    
    // Convert LIME list of tuples [["word", score], ...] to a score map
    const scores = {};
    explanation.forEach(([word, score]) => {
        scores[word.toLowerCase()] = score;
    });
    
    const verdictClass = isClickbait ? "verdict-red" : "verdict-green";
    const verdictText = isClickbait ? "Clickbait Detected" : "Looks Safe";
    
    let html = `
        <div class="cb-header">
            <span class="cb-title">AI Interpretation (LIME)</span>
            <span class="cb-verdict ${verdictClass}">${verdictText}</span>
        </div>
        <div class="cb-explanation">
    `;
    
    const words = text.split(/\s+/);
    words.forEach(word => {
        const cleanWord = word.toLowerCase().replace(/[^a-z0-9]/g, '');
        const score = scores[cleanWord] || 0;
        
        let style = "";
        let extraClass = "";
        
        if (score > 0) { 
            // Positive score supports the predicted class (Clickbait) -> RED
            const alpha = Math.min(Math.abs(score) * 15, 1.0);
            style = `style="background: rgba(220, 38, 38, ${alpha}); color: ${alpha > 0.4 ? 'white' : 'inherit'}"`;
            extraClass = "cb-high-clickbait";
        } else if (score < 0) {
            // Negative score opposes the predicted class (Clickbait) -> GREEN
            const alpha = Math.min(Math.abs(score) * 15, 1.0);
            style = `style="background: rgba(22, 163, 74, ${alpha}); color: ${alpha > 0.4 ? 'white' : 'inherit'}"`;
            extraClass = "cb-high-safe";
        }
        
        html += `<span class="cb-word-pill ${extraClass}" ${style}>${word}</span> `;
    });
    
    html += `</div>
        <div class="cb-footer">
            <span class="cb-confidence-label">AI Confidence Level</span>
            <span class="cb-confidence-val">${(confidence * 100).toFixed(1)}%</span>
        </div>
        <div class="cb-hint">High intensity colors highlight the most influential keywords.</div>
    `;
    
    tooltip.innerHTML = html;
}

function hideTooltip() {
    tooltip.classList.remove('cb-visible');
}

const observer = new MutationObserver((mutations) => {
    if (!isEnabled) return;
    let newNodes = false;
    mutations.forEach(m => { if (m.addedNodes.length > 0) newNodes = true; });
    
    if (newNodes) {
        if (window.cbTimeout) clearTimeout(window.cbTimeout);
        window.cbTimeout = setTimeout(scanHeadlines, 1500);
    }
});
observer.observe(document.body, { childList: true, subtree: true });
