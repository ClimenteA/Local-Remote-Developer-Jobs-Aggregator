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



var applyed = false

function save_applyed(event){

    // event.preventDefault()
    
    let job_id = event.target.parentElement.parentElement.id
    
    m.request({
        method: "PUT",
        url: `${document.location.origin}/update-job-status/${job_id}/${job_status}`,
        body: {job_id, job_status},
    })
    .catch(res => {
        console.error(res)
        
        m.mount(document.body, 
            m(Notification, 
                {notif_type:"is-danger", 
                notif_msg: res 
            }))
    })

}


// const Apply = () => {
    

//     return {

//         oninit: v => {
            
//             if (v.attrs.status === "applied") {
//                 applyed = true
//             }
//             else {
//                 applyed = false
//             }
//         },

//         view: v => {
                    
//             return m(
//                 applyed ? "button.button.is-disabled.ml-5" : "a.button.is-danger.ml-5", 
//                 {href: v.attrs.link, target: "_blank", 
//                  disabled: applyed,
//                  onclick: ev => save_applyed(ev)
//                 }, 
//                 applyed ? "Already viewed this job" : "View this job"  
//             )
//         }
//     }
// }


var ALL_JOB_LIST

function get_job_list(page_nbr) {

    m.request({
        method: "GET",
        url: `${document.location.origin}/all-jobs/${page_nbr}`
    })
    .then(jobs => {
        ALL_JOB_LIST = jobs["jobs"]
    }) 

}


/* <div class="select">
<select>
  <option>Select dropdown</option>
  <option>With options</option>
</select>
</div> */


const JobAction = {
    view: v => {
        console.log(v.attrs)
        
        return m(".select.ml-3", 
            
            m("select", 
                { name:"job-action", 
                  onchange: () => console.log("option changed!")}, 
                
                 [
                    m("option", 
                    {selected: true, disabled: true}, 
                    "Select action"
                    ),

                    m("option", 
                    {value: "Apply to this job"}, 
                    "Apply to this job"
                    ),

                    m("option", 
                    {value: "Not a job for me"}, 
                    "Not a job for me"
                    )
                ]
            )
        )

    }
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
                    m(JobAction, 
                        {link: job.link, status: job.status, job_id: job.id}),
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
            ALL_JOB_LIST ? m(JobList, {"jobs": ALL_JOB_LIST}) 
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

