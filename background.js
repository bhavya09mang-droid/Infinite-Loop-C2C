// Background Relay: Event-driven Service Worker
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "scanText") {
    
    // Route the fetch request to your local Flask backend
    fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        url: message.url,
        text: message.text,
        timestamp: message.timestamp
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log("Threat analysis received:", data);
      sendResponse({ status: "success", data: data });
    })
    .catch(error => {
      console.error("Error connecting to Guardian backend:", error);
      sendResponse({ status: "error", message: error.message });
    });

    return true; // Keeps the message channel open for the asynchronous response
  }
});