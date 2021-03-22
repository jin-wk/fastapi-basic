from functools import lru_cache
from pydantic import BaseSettings


class Setting(BaseSettings):
    APP_NAME: str
    APP_VERSION: str

    LOG_LEVEL: str

    DATABASE_HOST: str
    DATABASE_PORT: str
    DATABASE: str
    USERNAME: str
    PASSWORD: str

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_setting(env: str) -> BaseSettings:
    return Setting()
