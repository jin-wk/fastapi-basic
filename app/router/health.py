import os

from fastapi import APIRouter

from core.setting import get_setting

APP_ENV = os.getenv("APP_ENV")
setting = get_setting(APP_ENV)
router = APIRouter()


@router.get("/check")
async def health_check() -> str:
    return f"{APP_ENV} - {setting.APP_VERSION}"
