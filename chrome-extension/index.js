
document.getElementById("open-tabs").addEventListener("click", () => {
    chrome.storage.sync.clear()
    chrome.runtime.sendMessage({ msg: "startScrapping" })
})


document.getElementById("reset-state").addEventListener("click", () => {
    chrome.storage.sync.clear()
})

