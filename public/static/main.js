import RemoteJobs from "./App.js"
import Stats from "./components/Stats.js"
import Error404 from "./components/Error404.js"


m.route(document.getElementById("app"), "/", 
{
    "/": {
        onmatch: function() {
          m.route.set("/rjobs/new/1", null, {state: {key: Date.now()}})            
        }
    },
    "/rjobs/:categ/:page_nbr": RemoteJobs,                
    "/rjobs/stats": Stats,                
    "/:404...": Error404,  
})

