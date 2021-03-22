from fastapi import Request, APIRouter, Depends
from starlette_context import context
from app.router import base, health


async def req_body(req: Request) -> None:
    if str(req.method) == "POST":
        context.update(req_body=await req.json())

router = APIRouter()
router.include_router(base)
router.include_router(
    health.router,
    prefix="/api/health",
    tags=["health"],
    dependencies=[Depends(req_body)],
)
