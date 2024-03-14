import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from multiprocessing import cpu_count
from common.sqlite import init_db
from apps import routers
from config import cfg
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="RestAPI", description="Useful RestAPI's", lifespan=lifespan)


@app.get("/")
def it_works():
    return RedirectResponse("/remote-jobs", status_code=302)


[app.include_router(router) for router in routers]

app.mount("/public", StaticFiles(directory="public"), name="public")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[url.strip() for url in cfg.ALLOWED_ORIGINS.split(" ") if url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS", "DELETE"],
)


@app.exception_handler(StarletteHTTPException)
async def exception_handler(request: Request, exc: StarletteHTTPException):
    return RedirectResponse("/", status_code=302)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["strict-transport-security"] = (
        "max-age=63072000; includeSubdomains; preload"
    )
    response.headers["x-frame-options"] = "SAMEORIGIN"
    response.headers["x-content-type-options"] = "nosniff"
    response.headers["x-xss-protection"] = "0"
    response.headers["referrer-policy"] = "no-referrer, strict-origin-when-cross-origin"
    return response


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=cfg.HOST,
        port=cfg.PORT,
        reload=cfg.DEBUG,
        proxy_headers=True,
        forwarded_allow_ips="*",
        workers=cpu_count(),
    )
