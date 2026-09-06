document.addEventListener('DOMContentLoaded', async () => {
  let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  
  if (tab && tab.url) {
    document.getElementById('page-url').textContent = new URL(tab.url).hostname;
  }

  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => document.body.innerText
  }, (results) => {
    if (results && results[0]) {
      const pageText = results[0].result;
      
      fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: tab.url, text: pageText })
      })
      .then(response => response.json())
      .then(data => {
        document.getElementById('score-val').textContent = Math.round(data.threat_score * 100);
        
        if (data.threat_score > 0.5) {
          document.getElementById('risk-status').textContent = "High Risk Detected";
          document.getElementById('risk-desc').textContent = "Multiple manipulative UI tactics found.";
        } else {
          document.getElementById('risk-status').textContent = "Verified Safe";
          document.getElementById('risk-desc').textContent = "No deceptive patterns found on this page.";
          const circle = document.querySelector('.score-circle');
          if (circle) circle.style.borderColor = "#10b981";
        }
      })
      .catch(err => console.error("Backend offline:", err));
    }
  });
});