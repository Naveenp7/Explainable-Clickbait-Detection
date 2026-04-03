const API_URL = "http://localhost:8000";

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.type === "PREDICT") {
        fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ headlines: request.headlines })
        })
        .then(res => res.json())
        .then(data => sendResponse({ success: true, data: data }))
        .catch(err => sendResponse({ success: false, error: err.message }));
        return true;
    }
    
    if (request.type === "EXPLAIN") {
        fetch(`${API_URL}/explain`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ headline: request.headline })
        })
        .then(res => res.json())
        .then(data => sendResponse({ success: true, data: data }))
        .catch(err => sendResponse({ success: false, error: err.message }));
        return true;
    }
});
