import RemoteJobs from "./App.js"
import Error404 from "./components/Error404.js"


m.route(document.getElementById("app"), "/", 
{
    "/": {
        onmatch: function() {
          m.route.set('/new-jobs/1', null, {state: {key: Date.now()}})            
        }
      },
    "/new-jobs/:page_nbr": RemoteJobs,                
    "/all-jobs/:page_nbr": RemoteJobs,
    "/applied-jobs/:page_nbr": RemoteJobs,
    "/ignored-jobs/:page_nbr": RemoteJobs,
    "/:404...": Error404,  
})

