from fastapi import APIRouter
from core.connection import Connection

base = APIRouter()
local = Connection("local")


@base.on_event("startup")
async def connect():
    await local.connect()


@base.on_event("shutdown")
async def disconnect():
    await local.disconnect()
