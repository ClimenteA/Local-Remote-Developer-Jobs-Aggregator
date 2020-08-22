from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models import (
    Jobs, 
    Users, 
    UserApplications
)

app = FastAPI()
app.mount("/public", StaticFiles(directory="public"), name="public")
templates = Jinja2Templates(directory="public")

@app.get("/", response_class = HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request })


@app.get("/all-jobs/{page_nbr}")
async def all_jobs(page_nbr: int = 1):
    """ Show all available jobs """
    query = Jobs.select()\
                .order_by(Jobs.date.desc())\
                .paginate(page_nbr) 

    return [j for j in query.dicts()] 


@app.get("/applied-jobs/{page_nbr}")
async def applied_jobs(page_nbr: int = 1):
    """ Show all applied jobs """
    query = Jobs.select()\
            .where(Jobs.status == 'applied')\
            .order_by(Jobs.date.desc())\
            .paginate(page_nbr)    

    return [j for j in query.dicts()] 


@app.get("/ignored-jobs/{page_nbr}")
async def ignored_jobs(page_nbr: int = 1):
    """ Show all ignored jobs """
    query = Jobs.select()\
                .where(Jobs.status == 'ignored')\
                .order_by(Jobs.date.desc())\
                .paginate(page_nbr)    

    return [j for j in query.dicts()] 


@app.get("/new-jobs/{page_nbr}")
async def ignored_jobs(page_nbr: int = 1):
    """ Show all ignored jobs """
    query = Jobs.select()\
                .where( (Jobs.status != 'ignored') &  (Jobs.status != 'applied') )\
                .order_by(Jobs.date.desc())\
                .paginate(page_nbr)    

    return [j for j in query.dicts()] 


@app.put("/update-job-status/{job_id}/{job_status}") 
async def update_job_status(job_id: int, job_status: str):
    """ Update the status of a job application """
    selected_job = Jobs.get(Jobs.id == job_id)
    selected_job.status = job_status
    selected_job.save()
    return {"status": job_status}






# @app.get("/tech-jobs")
# async def tech_jobs():
#     """ Show available tech jobs """
#     return {"tech-jobs": "programing jobs"}


# @app.get("/custumer-support-jobs")
# async def customer_support_jobs():
#     """ Show available custumer support jobs """
#     return {"custumer-support": "custumer-support jobs"}


# @app.get("/other-jobs")
# async def other_jobs():
#     """ Show available other type of jobs """
#     return {"other": "other types of jobs"}



