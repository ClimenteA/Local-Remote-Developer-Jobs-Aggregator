








const JobAction = {
    view: v => {

        // console.log(v.attrs)

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


export default JobAction