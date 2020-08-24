
const JobDescription = () => {
    
    let show_description = false

    function toggle_description(event){
        show_description = !show_description
        event.target.parentElement.parentElement.scrollIntoView({behavior: "smooth"})
    }

    function make_paragraphs(raw_text){
        raw_text = raw_text.replace(/\n/g, '<br>')
        return m.trust("<div class='job-description' style='white-space: pre-line;'>" + raw_text + "</div>")
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


export default JobDescription