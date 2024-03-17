from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request
from common.sqlite import SqliteDBDep
from common.render_template import render_template

router = APIRouter(tags=["RemoteJobs"], prefix="/remote-jobs")


@router.get("/new", response_class=HTMLResponse)
async def get_new_jobs(request: Request, session: SqliteDBDep):
    return await render_template(
        request, "rjobs/index.html", context={"active_page": "new", "jobs": []}
    )


@router.get("/applied", response_class=HTMLResponse)
async def get_applied_jobs(request: Request, session: SqliteDBDep):
    return await render_template(
        request,
        "rjobs/index.html",
        context={"active_page": "applied", "jobs": []},
    )


@router.get("/ignored", response_class=HTMLResponse)
async def get_ignored_jobs(request: Request, session: SqliteDBDep):
    return await render_template(
        request,
        "rjobs/index.html",
        context={"active_page": "ignored", "jobs": []},
    )
