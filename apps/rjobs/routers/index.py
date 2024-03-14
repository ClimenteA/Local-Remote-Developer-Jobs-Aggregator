from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request
from common.sqlite import SqliteDBDep
from common.render_template import render_template
from apps.rjobs.models.job import Job
from apps.rjobs.views.job import add_jobs, get_all_jobs

router = APIRouter(tags=["RemoteJobs"], prefix="/remote-jobs")


@router.get("/", response_class=HTMLResponse)
async def get_index_template(request: Request, session: SqliteDBDep):
    # TODO Get jobs from DB
    jobs = [
        Job(
            title="Software Eng1", description="The best software eng", link="http etc"
        ),
        Job(
            title="Software Eng2", description="The best software eng", link="http etc"
        ),
        Job(
            title="Software Eng3", description="The best software eng", link="http etc"
        ),
    ]

    add_jobs(session, jobs)

    saved_jobs = get_all_jobs(session)

    return await render_template(
        request, "rjobs/index.html", context={"jobs": saved_jobs}
    )
