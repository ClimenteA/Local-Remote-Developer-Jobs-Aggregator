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


async function getReactJobsJobs() {

    const data = []
    for (const link of document.querySelectorAll("a")) {

        if (link.getAttribute("href").startsWith("https://reactjobs.io/react-jobs/")) {

            const title = link.textContent.replaceAll("\n", "").trim()
            if (title == "View") continue

            data.push({
                url: link.href,
                title: title,
                source: document.location.host
            })
        }
    }

    return data

}



async function getDevJobJobs() {

    let resp = await fetch("https://devjob.ro/api/jobsLight", { "method": "GET" })
    let data = await resp.json()

    const jobs = []
    for (const job of data) {

        if (!job.isFullRemote) continue

        const jobUrl = "https://devjob.ro/jobs/" + job.jobUrl

        jobs.push({
            url: jobUrl,
            title: job.name,
            source: document.location.host
        })
    }

    return jobs

}


async function getEuRemoteJobsJobs() {

    const headers = {
        "accept": "*/*",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43"
    }

    const data = {
        "lang": "",
        "search_categories[]": "engineering",
        "search_keywords": "",
        "search_location": "",
        "per_page": "12",
        "orderby": "featured",
        "order": "DESC",
        "show_pagination": "false"
    }

    const url = "https://euremotejobs.com/jm-ajax/get_listings/"

    const titleRegex = /data-title=\"(.*?)\"/g
    const urlRegex = /data-href=\"(.*?)\"/g

    const jobs = []
    for (let page = 1; page <= 3; page++) {
        data["page"] = String(page)

        const response = await fetch(url, {
            method: "POST",
            headers: headers,
            body: new URLSearchParams(data)
        });

        const responseData = await response.json()

        const titleMatches = [...responseData.html.matchAll(titleRegex)]
        const urlMatches = [...responseData.html.matchAll(urlRegex)]

        if (titleMatches.length == 0) continue
        if (urlMatches.length == 0) continue

        for (let i = 0; titleMatches.length > i; i++) {
            const title = titleMatches[i][1]
            const url = urlMatches[i][1]

            jobs.push({
                url: url,
                title: title,
                source: document.location.host
            })
        }
    }

    return jobs
}



async function getRemoteCoJobs() {

    const links = document.querySelectorAll("a.card.m-0.border-left-0.border-right-0.border-top-0.border-bottom")

    const data = []
    for (const link of links) {

        if (link.getAttribute("href").startsWith("/job/")) {

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


async function getWeWorkRemotelyJobs() {

    const data = []
    for (const link of document.querySelectorAll("a")) {
        const href = link.getAttribute("href")

        if (!href) continue
        if (!href.startsWith("/remote-jobs/")) continue

        const title = link.querySelector("span.title")
        if (!title) continue

        data.push({
            url: link.href,
            title: title.textContent,
            source: document.location.host
        })

    }

    return data
}


async function getWorkingNomadsJobs() {

    const response = await fetch("https://www.workingnomads.com/jobsapi/_search?track_total_hits=true&sort=premium:desc,pub_date:desc&_source=company,company_slug,category_name,locations,location_base,salary_range,salary_range_short,number_of_applicants,instructions,id,external_id,slug,title,pub_date,tags,source,apply_option,apply_email,apply_url,premium,expired,use_ats,position_type&size=100&from=0&q=(category_name.raw:%22Development%22)%20AND%20(locations:%22Anywhere%22%20OR%20locations:%22EU%22%20OR%20locations:%22Europe%22%20OR%20locations:%22EMEA%22%20OR%20locations:%22Spain%22%20OR%20locations:%22Portugal%22%20OR%20locations:%22Netherlands%22%20OR%20locations:%22Poland%22%20OR%20locations:%22Germany%22%20OR%20locations:%22Belgium%22%20OR%20locations:%22Czechia%22%20OR%20locations:%22Bulgaria%22%20OR%20locations:%22Ireland%22%20OR%20locations:%22Italy%22%20OR%20locations:%22Romania%22%20OR%20locations:%22Slovakia%22%20OR%20locations:%22Switzerland%22%20OR%20locations:%22Ukraine%22)", {
        "headers": {
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9,ro;q=0.8",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin"
        },
        "referrer": "https://www.workingnomads.com/jobs?category=development&location=anywhere,europe",
        "referrerPolicy": "same-origin",
        "body": null,
        "method": "GET",
        "mode": "cors",
        "credentials": "include"
    })

    const data = await response.json()

    const jobs = []
    for (const job of data.hits.hits) {

        if (!job._source.slug) continue

        const jobUrl = "https://www.workingnomads.com/jobs/" + job._source.slug

        jobs.push({
            url: jobUrl,
            title: job._source.title,
            source: document.location.host
        })
    }

    return jobs

}



const mapper = {
    "vuejobs.com": getVueJobs,
    "www.ejobs.ro": getEjobsJobs,
    "www.bestjobs.eu": getBestJobsJobs,
    "jsjobbs.com": getJsJobbsJobs,
    "remotive.com": getRemotiveJobs,
    "remoteok.com": getRemoteOkJobs,
    "reactjobs.io": getReactJobsJobs,
    "devjob.ro": getDevJobJobs,
    "euremotejobs.com": getEuRemoteJobsJobs,
    "remote.co": getRemoteCoJobs,
    "weworkremotely.com": getWeWorkRemotelyJobs,
    "www.workingnomads.com": getWorkingNomadsJobs
}



mapper[document.location.host]().then(results => {
    console.log(results)
})
