var stats = undefined


function get_stats() {
    m.request({
        method: "GET",
        url: `${document.location.origin}/rjobs/stats`
    })
    .then(data => {
        stats = data
        console.log(stats)
    }) 
}


const Stats = {

    oninit: v => {
        get_stats()
    },

    view: v => {
        
        return stats ? 
        m(".section", "Here are the stats") : 
        m("span", "Stats loading...")
           
    }
}


export default Stats