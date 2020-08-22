import RemoteJobs from "./App.js"
import Error404 from "./components/Error404.js"


m.route(document.getElementById("app"), "/", 
{
    "/": {
        onmatch: function() {
          m.route.set('/all-jobs/1')
        }
      },
    "/all-jobs/:page_nbr": RemoteJobs,
    "/:404...": Error404,  
})

