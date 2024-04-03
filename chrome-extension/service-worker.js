
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.msg === "tab_close_msg") {
        chrome.tabs.remove(sender.tab.id, function () {
            sendResponse({ status: "Tab closed" })
        })
    }
})
