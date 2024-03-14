import typing
from fastapi import Request
from fastapi.templating import Jinja2Templates
from common.logger import log

templates = Jinja2Templates(directory="templates")


async def render_template(
    request: Request,
    name: str,
    context: dict = None,
    status_code: int = 200,
    headers: typing.Optional[typing.Mapping[str, str]] = None,
    media_type: typing.Optional[str] = None,
):
    try:
        if context is None:
            context = {}

        context.update({"current_template": name})

        return templates.TemplateResponse(
            name=name,
            context={**{"request": request}, **context},
            status_code=status_code,
            headers=headers,
            media_type=media_type,
        )
    except Exception as err:
        log.exception(err)

    return templates.TemplateResponse(
        name="FAILED.html",
        context={"request": request},
        status_code=500,
    )
