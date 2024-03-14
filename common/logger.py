import os
from loguru import logger as log
from config import cfg

logpath = os.path.join(cfg.STORAGE_PATH, "logs.log")


if cfg.DEBUG and os.path.exists(logpath):
    os.remove(logpath)

log.add(
    logpath,
    enqueue=True,
    level="DEBUG" if cfg.DEBUG else cfg.LOG_LEVEL,
    retention=cfg.LOG_RETENTION,
)
