#Update database with latest jobs
# import remoter

import uvicorn
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


@app.get("/rjobs/{categ}/{page_nbr}")
async def all_jobs(categ: str = "new", page_nbr: int = 1):
    """ 
        Show available remote jobs for the choosen category
    """
    
    if categ == "new":
        query = Jobs.select().where( (Jobs.status != 'ignored') & (Jobs.status != 'applied') ).order_by(Jobs.date.desc()).paginate(page_nbr)    
    elif categ == "all":
        query = Jobs.select().order_by(Jobs.date.desc()).paginate(page_nbr) 
    elif categ == "applied":
        query = Jobs.select().where(Jobs.status == 'applied').order_by(Jobs.date.desc()).paginate(page_nbr)    
    elif categ == "ignored":
        query = Jobs.select().where(Jobs.status == 'ignored').order_by(Jobs.date.desc()).paginate(page_nbr)    

    return [j for j in query.dicts()] 


@app.get("/rjobs/stats")
async def stats():

    applied = Jobs.select().where(
        (Jobs.status == 'applied') & 
        (Jobs.description.contains("python"))
        )    

    # ignored = Jobs.select().where(Jobs.status == 'ignored')    

    return {
        applied: [j for j in applied.dicts()],
        # ignored: [j for j in ignored.dicts()]
    } 


@app.put("/update-job-status/{job_id}/{job_status}") 
async def update_job_status(job_id: int, job_status: str):
    """ 
        Update the status of a job application 
    """
    selected_job = Jobs.get(Jobs.id == job_id)
    selected_job.status = job_status
    selected_job.save()
    return {"status": job_status}



def get_server_ip():
    """Get ip address of current device"""
    import socket
    ip = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
    return ip


this_pc_ip = get_server_ip()


@app.get("/mock")
async def root():
    return {"hello": "world"}



if __name__ == '__main__':
    print("\nConnect to:", this_pc_ip, ":5000\n")
    uvicorn.run(app, host="0.0.0.0", port=5000)
    # gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
