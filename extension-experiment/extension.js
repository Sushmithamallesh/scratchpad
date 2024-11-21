// Configuration
let blockedSites = [];
let workingHours = { start: '09:00', end: '12:00' };
let breakDuration = 5 * 60 * 1000; // 5 minutes in milliseconds

// Main functionality
function initExtension() {
    chrome.storage.sync.get(['blockedSites', 'workingHours'], (result) => {
        blockedSites = result.blockedSites || [];
        workingHours = result.workingHours || workingHours;
        setupListeners();
    });
}

function setupListeners() {
    chrome.webNavigation.onBeforeNavigate.addListener(checkIfBlocked);
    chrome.alarms.onAlarm.addListener(handleAlarm);
}

function checkIfBlocked(details) {
    if (isBlockedSite(details.url) && isWithinWorkingHours()) {
        chrome.tabs.update(details.tabId, { url: chrome.runtime.getURL("blocked.html") });
    }
}

function isBlockedSite(url) {
    return blockedSites.some(site => url.includes(site));
}

function isWithinWorkingHours() {
    // Implementation to check current time against working hours
}

function unblockTemporarily(site) {
    // Implement unblocking logic
    chrome.alarms.create('reblock', { delayInMinutes: 5 });
}

function handleAlarm(alarm) {
    if (alarm.name === 'reblock') {
        // Re-implement blocking
        displayReminder();
    } else if (alarm.name === 'endBreak') {
        endBreak();
    }
}

function startBreak() {
    // Implement break start logic
    chrome.alarms.create('endBreak', { delayInMinutes: 5 });
}

function endBreak() {
    // Implement break end logic
    displayWorkReminder();
}

function displayReminder() {
    // Display reminder to get back to work
}

function displayWorkReminder() {
    // Display custom work reminder image
}

initExtension();