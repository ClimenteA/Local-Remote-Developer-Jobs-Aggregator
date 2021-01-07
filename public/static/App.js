import Pagination from "./components/Pagination.js"
import JobDescription from "./components/JobDescription.js"
import JobAction from "./components/JobAction.js"


var store = {
    job_list: undefined
}

function get_job_list(data) {
    // Get jobs in chunks of 20 per page

    m.request({
        method: "GET",
        url: `${document.location.origin}/rjobs/${data.categ}/${data.page_nbr}`
    })
    .then(jobs => {
        store.job_list = jobs
        // console.log(store.job_list)
    }) 

}


const JobList = {     
    
    view: v => {

        if (v.attrs.jobs.length === 0) {
            return m(".box.has-background-warning.mt-3", 
                    "No jobs available in this category.")
        }

        return m("ul.min-100-vh", v.attrs.jobs.map(job => {
            return m("li.my-6", { key:job.id, id:job.id },     
            m(".job-card", 
                [
                    m("span.tag.is-pulled-right", job.status),
                    m("h4.title.is-4", job.title),
                    m("h6.subtitle.is-6", job.company),
                
                    m(JobAction, 
                        {  
                            link: job.link, 
                            status: job.status, 
                            job_id: job.id
                        }),
                    
                    
                    m(JobDescription, 
                        {description: job.description}),

                    
                ])    
            )
        }))
    }
}



const RemoteJobs = {
    
    oninit: v => {
        get_job_list(v.attrs)
    },
    
    view: v => {
        return [
            m("h1.title.is-2", "Remote jobs"), 
            
            m("span.ml-3.tag.hand.is-link", {onclick: _ => {
                m.route.set("/rjobs/new/1", null, {state: {key: Date.now()}})
            }}, "New"),

            m("span.ml-3.tag.hand.is-link", {onclick: _ => {
                m.route.set("/rjobs/all/1", null, {state: {key: Date.now()}})
            }}, "All"),
              
            m("span.ml-3.tag.hand.is-link", {onclick: _ => {
                m.route.set("/rjobs/applied/1", null, {state: {key: Date.now()}})
            }}, "Applied"),
              
            m("span.ml-3.tag.hand.is-link", {onclick: _ => {
                m.route.set("/rjobs/ignored/1", null, {state: {key: Date.now()}})
            }}, "Ignored"),

            m("span.ml-3.tag.hand.is-link", {onclick: _ => {
                m.route.set("/rjobs/stats", null, {state: {key: Date.now()}})
            }}, "Stats"),

            store.job_list ? m(JobList, {jobs: store.job_list})
            : m(".box.has-background-warning.mt-3", "Loading all jobs..."),
            m(Pagination, {categ: v.attrs.categ, page_nbr: v.attrs.page_nbr})
        ]
    }
}


export default RemoteJobs