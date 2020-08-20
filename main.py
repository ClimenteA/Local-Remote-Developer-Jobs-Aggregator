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
    query = Jobs.select().paginate(page_nbr)    
    return {"jobs": [j for j in query.dicts()]}



@app.get("/tech-jobs")
async def tech_jobs():
    """ Show available tech jobs """
    return {"tech-jobs": "programing jobs"}


@app.get("/custumer-support-jobs")
async def customer_support_jobs():
    """ Show available custumer support jobs """
    return {"custumer-support": "custumer-support jobs"}


@app.get("/other-jobs")
async def other_jobs():
    """ Show available other type of jobs """
    return {"other": "other types of jobs"}


@app.put("/job/{job_id}")
async def update_job(job_id: int):
    """ Update the status of a job application """
    return {"other": "other types of jobs"}

