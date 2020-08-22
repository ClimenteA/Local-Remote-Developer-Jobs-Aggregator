
function open_link_in_new_tab(url){
    let a = document.createElement("a")
    a.setAttribute("target", "_blank")
    a.setAttribute("href", url)
    a.click()
}


function update_job_status(event, data) {
    
    console.log("DATA: ", data)
    event.redraw = false

    let status = event.target.value

    m.request({
        method: "PUT",
        url: `${document.location.origin}/update-job-status/${data.job_id}/${status}`,
        body: {job_id: data.job_id, job_status: status},
    })
    .then( res => {
        
        if (res.status === "applied"){
            open_link_in_new_tab(data.link)
        }
        
        document.getElementById(data.job_id).querySelector(".tag").innerText = status

    })

}


const JobAction = {
    
    view: v => {

        return m(".select.ml-3", 
            
            m("select", 
                { name:"job-action", onchange: ev => update_job_status(ev, v.attrs) },
                
                 [
                    m("option", 
                    {value: "new"}, 
                    "Select action"
                    ),

                    m("option", 
                    {value: "applied"}, 
                    "View this job"
                    ),

                    m("option", 
                    {value: "ignored"}, 
                    "Ignore this job"
                    )
                ]
            )
        )

    }
}


export default JobAction