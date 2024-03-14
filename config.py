from pydantic_settings import BaseSettings


DEVUSER = "admin"
DEVPASS = "secretpass"
DB = "DB"


class Config(BaseSettings):
    ADMIN_EMAIL: str = DEVUSER
    ADMIN_PASSWORD: str = DEVPASS
    ADMIN_USERNAME: str = DEVUSER
    STORAGE_PATH: str = "./"
    ALLOWED_ORIGINS: str = "*"
    DBLOCAL: bool = False
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    LOG_LEVEL: str = "ERROR"
    LOG_RETENTION: str = "1 week"
    PORT: int = 3000
    SECRET: str = DEVPASS


cfg = Config()
