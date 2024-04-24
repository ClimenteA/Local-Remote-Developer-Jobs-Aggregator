
document.getElementById("open-tabs").addEventListener("click", () => {
    chrome.storage.sync.clear()
    chrome.storage.sync.set({ 'contentScriptStatus': 'active' })
    chrome.runtime.sendMessage({ msg: "startScrapping" })
})


document.getElementById("reset-state").addEventListener("click", () => {
    chrome.storage.sync.clear()
})


const contentScriptTextElem = document.getElementById("content-script-text")
const contentScriptStatusElem = document.getElementById("content-script-status")
const inactiveText = "Inactive content script"
const activeText = "Active content script"


contentScriptStatusElem.addEventListener("click", () => {

    chrome.storage.sync.get(['contentScriptStatus'], function (items) {

        if (!items.contentScriptStatus?.length > 0) {
            items.contentScriptStatus = 'active'
        }

        if (items.contentScriptStatus == 'active') {
            chrome.storage.sync.set({ 'contentScriptStatus': 'inactive' })
            contentScriptTextElem.innerText = inactiveText
            contentScriptStatusElem.checked = false
            return
        }

        if (items.contentScriptStatus == 'inactive') {
            chrome.storage.sync.set({ 'contentScriptStatus': 'active' })
            contentScriptTextElem.innerText = activeText
            contentScriptStatusElem.checked = true
            return
        }

    })

})


chrome.storage.sync.get(['contentScriptStatus'], function (items) {

    if (!items.contentScriptStatus?.length > 0) {
        items.contentScriptStatus = 'active'
    }

    if (items.contentScriptStatus == 'active') {
        chrome.storage.sync.set({ 'contentScriptStatus': 'active' })
        contentScriptTextElem.innerText = activeText
        contentScriptStatusElem.checked = true
        return
    }

    if (items.contentScriptStatus == 'inactive') {
        chrome.storage.sync.set({ 'contentScriptStatus': 'inactive' })
        contentScriptTextElem.innerText = inactiveText
        contentScriptStatusElem.checked = false
        return
    }

})