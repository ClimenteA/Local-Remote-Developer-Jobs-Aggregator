from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request
from common.render_template import render_template


router = APIRouter(tags=["RemoteJobs"], prefix="/remote-jobs")


@router.get("/", response_class=HTMLResponse)
async def get_index_template(request: Request):
    # TODO Get jobs from DB
    jobs = []
    return await render_template(request, "rjobs/index.html", context={"jobs": jobs})
