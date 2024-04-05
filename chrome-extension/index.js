
document.getElementById("open-tabs").addEventListener("click", () => {
    chrome.runtime.sendMessage({ msg: "startScrapping" })
    localStorage.setItem("closeTabs", "true")
})


const closeTabsCheckbox = document.getElementById("close-tabs")

closeTabsCheckbox.addEventListener("change", () => {
    localStorage.setItem("closeTabs", String(closeTabsCheckbox.checked))
})