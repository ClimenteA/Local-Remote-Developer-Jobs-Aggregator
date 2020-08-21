"use strict"

m.route.prefix = '#'


const Error404 = {
    view: function() {
        return m("h1.is-size-1.has-text-danger", "Page not found")
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
        return m.trust("<div class='job-description'>" + doc + "</div>")
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



const Notification = {
    view: v => {
        return m(`.notification.${v.attrs.notif_type}`, 
        [
            m("button.delete"),
            m("p", v.attrs.notif_msg)
        ])
    }
}


const Apply = () => {
    
    let applyed = false

    function save_applyed(event){

        // event.preventDefault()
        
        let job_id = event.target.parentElement.parentElement.id

        m.request({
            method: "PUT",
            url: `${document.location.origin}/update-job-status/${job_id}`,
            body: {job_id: job_id},
        })
        .catch(res => {
            console.error(res)
            
            m.mount(document.body, 
                m(Notification, 
                    {notif_type:"is-danger", 
                    notif_msg: res 
                }))
        })

        applyed = true
    }

    return {

        oninit: v => {
            
            if (v.attrs.status === "applied") {
                applyed = true
            }
            else {
                applyed = false
            }
        },

        view: v => {
                    
            return m(
                applyed ? "button.button.is-disabled.ml-5" : "a.button.is-danger.ml-5", 
                {href: v.attrs.link, target: "_blank", 
                 disabled: applyed,
                 onclick: ev => save_applyed(ev)
                }, 
                applyed ? "Already applyed to this job" : "Apply to this job"  
            )
        }
    }
}



var all_jobs_list

function get_job_list(page_nbr) {

    m.request({
        method: "GET",
        url: `${document.location.origin}/all-jobs/${page_nbr}`
    })
    .then(jobs => {
        all_jobs_list = jobs["jobs"]
        // console.log("This should be 20 per page. Page:", page_nbr, all_jobs_list) 
    }) 

}


const JobList = {
            
    view: v => {
        
        if (!v.attrs.jobs) {
            return m('div', 'Empty!')
        }
           
        return m("ul", v.attrs.jobs.map(job => {
            
            return m("li.my-6", {key:job.id, id:job.id}, m(".job-card", [
                    m("h4.title.is-4", job.title),
                    m("h6.subtitle.is-6", job.company),
                    m(JobDescription, {description: job.description}),
                    m(Apply, {link: job.link, status: job.status}),
                ])    
            )
        }))
    }
}


const AllJobs = {
    
    oninit: v => {
        get_job_list(v.attrs.page_nbr)
    },

    view: v => {
        return [
            m("h1.title.is-2", "Remote jobs"),       
            all_jobs_list ? m(JobList, {"jobs": all_jobs_list}) 
            : m("span.tag.is-warning.is-light", "Loading all jobs..."),
            m(NextPage, {page_nbr: v.attrs.page_nbr})
        ]
    }
}

const NextPage = {
    view: v => {
        
        let current_page = Number(v.attrs.page_nbr)
        
        return [
            m(".buttons.has-addons.is-centered", [
                m("button.button.is-primary", 
                { onclick: _ => {
                    m.route.set(`/all-jobs/${current_page - 1}`, null, {state: {key: Date.now()}})
                    window.scrollTo({top: 0}) 
                }},
                "< Prev"
                ),
                m("button.button.is-primary", 
                { onclick: _ => {
                    m.route.set(`/all-jobs/${current_page + 1}`, null, {state: {key: Date.now()}})
                    window.scrollTo({top: 0})    
                }},
                "Next >"
                ),
                
            ])
        ]
        
        
    }
}


const App = document.getElementById("app")

m.route(App, "/", {
    "/": {
        onmatch: function() {
          m.route.set('/all-jobs/1')
        }
      },
    "/all-jobs/:page_nbr": AllJobs,
    "/:404...": Error404,  
})

