
document.getElementById("open-tabs").addEventListener("click", () => {
    chrome.storage.sync.clear()
    chrome.storage.sync.set({ 'jobCollectionStatus': 'active' })
    chrome.runtime.sendMessage({ msg: "startScrapping" })
})


document.getElementById("reset-state").addEventListener("click", () => {
    chrome.storage.sync.clear()
})


// JOB COLLECTION FETCHING

const jobCollectionTextElem = document.getElementById("job-collection-fetching-text")
const jobCollectionStatusElem = document.getElementById("job-collection-fetching-status")
const inactiveText = "Inactive job collection"
const activeText = "Active job collection"


jobCollectionStatusElem.addEventListener("click", () => {

    chrome.storage.sync.get(['jobCollectionStatus'], function (items) {

        if (!items.jobCollectionStatus?.length > 0) {
            items.jobCollectionStatus = 'active'
        }

        if (items.jobCollectionStatus == 'active') {
            chrome.storage.sync.set({ 'jobCollectionStatus': 'inactive' })
            jobCollectionTextElem.innerText = inactiveText
            jobCollectionStatusElem.checked = false
            return
        }

        if (items.jobCollectionStatus == 'inactive') {
            chrome.storage.sync.set({ 'jobCollectionStatus': 'active' })
            jobCollectionTextElem.innerText = activeText
            jobCollectionStatusElem.checked = true
            return
        }

    })

})


chrome.storage.sync.get(['jobCollectionStatus'], function (items) {

    if (!items.jobCollectionStatus?.length > 0) {
        items.jobCollectionStatus = 'active'
    }

    if (items.jobCollectionStatus == 'active') {
        chrome.storage.sync.set({ 'jobCollectionStatus': 'active' })
        jobCollectionTextElem.innerText = activeText
        jobCollectionStatusElem.checked = true
        return
    }

    if (items.jobCollectionStatus == 'inactive') {
        chrome.storage.sync.set({ 'jobCollectionStatus': 'inactive' })
        jobCollectionTextElem.innerText = inactiveText
        jobCollectionStatusElem.checked = false
        return
    }

})