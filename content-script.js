console.log("Loaded:", document.location.host)


async function getVueJobs() {

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

async function getEjobsJobs() {

    const textContent = document.documentElement.outerHTML
    const regex = /id:(\d{7}),title:"(.*?)"/g

    let match
    const data = []
    while ((match = regex.exec(textContent)) !== null) {
        const id = match[1];
        const title = match[2];
        const slug = title.toLowerCase().replaceAll(" ", "-")
        const url = `https://www.ejobs.ro/user/locuri-de-munca/${slug}/${id}`
        data.push({
            url: url,
            title: title,
            source: document.location.host
        })
    }

    return data

}


async function getBestJobsJobs() {

    const data = []
    for (const link of document.querySelectorAll("a")) {
        if (link.getAttribute("href").startsWith("https://www.bestjobs.eu/ro/loc-de-munca/")) {
            data.push({
                url: link.href,
                title: link.querySelector("span").textContent,
                source: document.location.host
            })
        }
    }

    return data
}

async function getJsJobbsJobs() {

    const fetchOptions = {
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,ro;q=0.8",
            "authorization": "Bearer",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        },
        "referrer": "https://jsjobbs.com/jobs",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": null,
        "method": "GET",
        "mode": "cors",
        "credentials": "include"
    }

    const resp = await fetch("https://jsjobbs.com/api/jobs/published?pageNum=1&pageSize=100", fetchOptions)
    const data = await resp.json()

    const jobs = []
    for (const job of data.jobs) {
        jobs.push({
            url: job.applyLinkOrEmail,
            title: job.title,
            source: document.location.host
        })
    }

    return jobs

}


async function getRemotiveJobs() {

    let resp = await fetch("https://remotive.com/api/remote-jobs?category=software-dev", { "method": "GET" })
    let data = await resp.json()

    const jobs = []
    for (const job of data.jobs) {
        jobs.push({
            url: job.url,
            title: job.title,
            source: document.location.host
        })
    }

    return jobs

}


async function getRemoteOkJobs() {

    const data = []
    for (const link of document.querySelectorAll("a")) {

        if (link.getAttribute("href").startsWith("/remote-jobs/")) {

            const title = link.querySelector("h2")
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
    "www.bestjobs.eu": getBestJobsJobs,
    "jsjobbs.com": getJsJobbsJobs,
    "remotive.com": getRemotiveJobs,
    "remotive.com": getRemotiveJobs,
    "remoteok.com": getRemoteOkJobs
}



mapper[document.location.host]().then(results => {
    console.log(results)
})
