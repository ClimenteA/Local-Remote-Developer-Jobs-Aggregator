console.log("Loaded:", document.location.host)


function getVueJobs() {

    const data = []
    const titleSelector = "div.font-display.text-lg.leading-tight.font-bold"
    for (const link of document.querySelectorAll("a")) {
        if (link.getAttribute("href").startsWith("/jobs/")) {

            data.push({
                url: link.href,
                title: link.querySelector(titleSelector).textContent,
                source: document.location.host
            })

        }
    }

    return data

}

function getEjobsJobs() {

    console.log("Helooooooo NUXT:", window.__NUXT__.pinia.jobs.items.listItems)

    const data = []

    for (const link of document.querySelectorAll('a')) {

        if (link.getAttribute("href").startsWith("/user/locuri-de-munca/")) {

            const title = link.querySelector("span")

            if (!title) continue

            data.push({
                url: link.href,
                title: title.textContent,
                source: document.location.host
            })

        }
    }

    return data

}







const mapper = {
    "vuejobs.com": getVueJobs,
    "www.ejobs.ro": getEjobsJobs,
}


const results = mapper[document.location.host]()


console.log(results)


