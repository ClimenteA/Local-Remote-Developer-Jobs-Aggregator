
document.getElementById("open-tabs").addEventListener("click", () => {
    chrome.runtime.sendMessage({ msg: "startScrapping" })
})
