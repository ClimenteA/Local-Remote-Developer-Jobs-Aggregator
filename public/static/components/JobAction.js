
function open_link_in_new_tab(url){
    let a = document.createElement("a")
    a.setAttribute("target", "_blank")
    a.setAttribute("href", url)
    a.click()
}


function update_job_status(status, data) {
    
    m.request({
        method: "PUT",
        url: `${document.location.origin}/update-job-status/${data.job_id}/${status}`,
        body: {job_id: data.job_id, job_status: status},
    })
    .then( res => {
        
        if (res.status === "applied"){
            open_link_in_new_tab(data.link)
        }
        
        let tag = document.getElementById(data.job_id).querySelector(".tag")
        tag.innerText = status

    })

}



const JobAction = {
    
    view: v => {

        return [
            
            m("button.button.is-info.mb-2", 
            {onclick: _ => update_job_status("applied", v.attrs)}, 
            "APPLY"),

            m("button.button.is-warning.ml-3.mb-2", 
            {onclick: _ => update_job_status("ignored", v.attrs)}, 
            "IGNORE")
        ]
    }
}



export default JobAction