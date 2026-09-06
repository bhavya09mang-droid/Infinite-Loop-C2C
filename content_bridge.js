// Client Bridge: Zero-latency DOM extraction
const pageText = document.body ? document.body.innerText : "";

if (pageText.trim().length > 0) {
  // Asynchronous background relay
  chrome.runtime.sendMessage({
    action: "scanText",
    url: window.location.href,
    text: pageText,
    timestamp: Date.now()
  });
}