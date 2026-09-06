let latestScanResult = null;
let lastScannedText = null;
let scanInFlight = false;
let debounceTimer = null;

const API_URL = 'http://localhost:5000/api/scan';
const DEBOUNCE_MS = 800;

async function sendPageToAPI() {
  const pageText = document.body.innerText.trim();

  // Skip if nothing changed or empty
  if (!pageText || pageText === lastScannedText) return;

  // Skip if a request is already in flight
  if (scanInFlight) return;

  scanInFlight = true;
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);

    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: pageText }),
      signal: controller.signal
    });

    clearTimeout(timeout);

    if (response.ok) {
      latestScanResult = await response.json();
      lastScannedText = pageText;
      console.log('✅ Analysis from combined.py API:', latestScanResult);
    } else {
      console.warn('⚠️ API responded with status', response.status);
    }
  } catch (error) {
    if (error.name === 'AbortError') {
      console.error('❌ Scan request timed out');
    } else {
      console.error('❌ Unable to connect to combined.py API:', error);
    }
  } finally {
    scanInFlight = false;
  }
}

function scheduleScan() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(sendPageToAPI, DEBOUNCE_MS);
}

// Listen for requests from popup.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'GET_SCAN_RESULTS') {
    sendResponse(latestScanResult);
    return true; // keep channel open in case sendResponse is deferred elsewhere
  }
});

// Initial scan
scheduleScan();

// Re-scan on dynamic content changes (SPAs, lazy-loaded content), debounced
const observer = new MutationObserver(scheduleScan);
observer.observe(document.body, { childList: true, subtree: true, characterData: true });