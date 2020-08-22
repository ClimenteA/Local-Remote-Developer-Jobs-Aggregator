
const Pagination = {
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


export default Pagination