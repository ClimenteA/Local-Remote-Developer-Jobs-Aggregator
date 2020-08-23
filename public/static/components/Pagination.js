
const Pagination = {
    view: v => {
        
        let current_page = Number(v.attrs.page_nbr)
        let category = v.attrs.categ
        
        return [
            m(".buttons.has-addons.is-centered", [
                m("button.button.is-link.mr-3", 
                { onclick: _ => {
                    m.route.set(`/rjobs/${category}/${current_page - 1}`, null, {state: {key: Date.now()}})
                    window.scrollTo({top: 0}) 
                }},
                "< Prev"
                ),
                m("button.button.is-link", 
                { onclick: _ => {
                    m.route.set(`/rjobs/${category}/${current_page + 1}`, null, {state: {key: Date.now()}})
                    window.scrollTo({top: 0})    
                }},
                "Next >"
                ),
                
            ])
        ]
        
        
    }
}


export default Pagination