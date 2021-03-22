import os
from fastapi import FastAPI
from core.route import router
from core.middleware import Middleware
from core.handler import ExceptionHandler
from core.setting import get_setting

APP_ENV = os.getenv("APP_ENV")
get_setting.cache_clear()
setting = get_setting(APP_ENV)

docs_url = "/docs"
redoc_url = "/redoc"
if APP_ENV == "production":
    docs_url = None
    redoc_url = None

app = FastAPI(
    title=setting.APP_NAME,
    version="{}-{}".format(APP_ENV, setting.APP_VERSION),
    description="Basic Application by FastAPI",
    docs_url=docs_url,
    redoc_url=redoc_url,
)
app.include_router(router)

Middleware(app)
ExceptionHandler(app)
