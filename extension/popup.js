const toggle = document.getElementById('toggleExt');
const blurToggle = document.getElementById('toggleBlur');
const apiStatus = document.getElementById('apiStatus');
const statusText = document.getElementById('statusText');

chrome.storage.local.get(['extensionEnabled', 'blurEnabled', 'domainStats'], (res) => {
    toggle.checked = res.extensionEnabled !== false;
    blurToggle.checked = res.blurEnabled === true;

    // Update Quick Stats
    if (res.domainStats) {
        let total = 0, clickbait = 0;
        Object.values(res.domainStats).forEach(s => {
            total += s.total;
            clickbait += s.clickbait;
        });
        document.getElementById('statTotal').innerText = total;
        document.getElementById('statClickbait').innerText = clickbait;
    }
});

// Check API Status
fetch("http://localhost:8000/")
    .then(r => {
        apiStatus.className = "api-status status-online";
        statusText.innerText = "Online";
    })
    .catch(e => {
        apiStatus.className = "api-status status-offline";
        statusText.innerText = "Offline";
    });

toggle.addEventListener('change', (e) => {
    const isEnabled = e.target.checked;
    chrome.storage.local.set({ extensionEnabled: isEnabled });
    notifyTabs({action: "toggle", state: isEnabled});
});

blurToggle.addEventListener('change', (e) => {
    const isBlur = e.target.checked;
    chrome.storage.local.set({ blurEnabled: isBlur });
    notifyTabs({action: "blurToggle", state: isBlur});
});

document.getElementById('openAnalytics').addEventListener('click', () => {
    chrome.tabs.create({ url: 'analytics.html' });
});

function notifyTabs(msg) {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        if(tabs[0]) {
            chrome.tabs.sendMessage(tabs[0].id, msg, (res) => {
                if (chrome.runtime.lastError) console.log(chrome.runtime.lastError.message);
            });
        }
    });
}
