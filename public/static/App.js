"use strict"

m.route.prefix = '#'


const LandingPage = {

    view: function() {
        return m("h1", "LandingPage")
    }
}



const JobDescription = () => {
    
    let show_description = false

    function toggle_description(event){
        show_description = !show_description
        event.target.parentElement.parentElement.scrollIntoView({behavior: "smooth"})
    }

    function make_paragraphs(raw_text){
        let parts = raw_text.split(".");
        let doc = parts.join(".</p><p class='mb-2'>")
        return m.trust(doc)
    }
    
    return {
        view: v => {

            let description = make_paragraphs(v.attrs.description)

            return [
                m(`div.${show_description ? "is-block" : "is-hidden"}.mb-4`, description),            
                
                m("button.button.is-link", 
                { onclick: ev => toggle_description(ev) }, 
                show_description ? "Hide description" : "View description" ),
            ]
        }
    }
}


const Apply = () => {
    
    function save_applyed(event){
        // event.preventDefault()
        let clicked_job_id = event.target.parentElement.parentElement.id
        console.log("Applyed", clicked_job_id)
    
        event.target.disabled = true
        event.target.innerText = "Already applyed to this job"
        event.target.style.cursor = "default"
        event.target.classList.remove("is-danger")
        event.target.classList.add("is-disabled")
    }

    return {
        view: v => {
            return m(
                "a.button.is-danger.ml-5", 
                {href: v.attrs.link, target: "_blank", onclick: ev => save_applyed(ev)}, 
                "Apply to this job"
            )
        }
    }
}


const JobList = () => {
            
    return {
        view: v => {
                
            return m("ul", v.attrs.jobs.map(job => {
                
                return m("li.my-6", {key:job.id, id:job.id}, m(".job-card", [
                
                        m("h4.title.is-4", job.title),
                        m("h6.subtitle.is-6", job.company),
                        m(JobDescription, {description: job.description}),
                        m(Apply, {link: job.link}),
                    ]) 
                    
                )
    
            }))
        }

    }
}


const AllJobs = (page_nbr) => {
    
    let all_jobs_list

    function get_job_list(page_nbr) {

        m.request({
            method: "GET",
            url: `${document.location.origin}/all-jobs/${page_nbr}`
        })
    
        .then(jobs => {
            all_jobs_list = jobs["jobs"]
            page_nbr = page_nbr + 1
            console.log("Page:", page_nbr, all_jobs_list)
            m.redraw()
        })        
    }

    get_job_list(page_nbr)

    return {
        view: v => {

            return [
                m("h1.title.is-2", "AllJobs"),       
                all_jobs_list ? m(JobList, {"jobs": all_jobs_list}) 
                : m("span.tag.is-warning.is-light", "Loading all jobs...")
            ]
        }
    }
}


const TechJobs = {
    view: function() {
        return m("h1", "TechJobs")
    }
}


const CustomerSupportJobs = {
    view: function() {
        return m("h1", "CustomerSupportJobs")
    }
}


const OtherJobs = {
    view: function() {
        return m("h1", "OtherJobs")
    }
}


const Error404 = {
    view: function() {
        return m("h1", "Error404")
    }
}


const App = document.getElementById("app")

m.route(App, "/", {
    "/": m.route.set("/all-jobs/1"),
    "/all-jobs/:page_nbr": AllJobs,
    "/tech-jobs": TechJobs,
    "/custumer-support-jobs": CustomerSupportJobs,
    "/other-jobs": OtherJobs, 
    "/:404...": Error404,  
})


