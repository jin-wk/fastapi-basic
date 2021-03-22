import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette_context import context
from starlette_context.middleware import ContextMiddleware
from core.logger import Logger

logger = Logger().logger

origins = ["*"]
methods = ["GET", "POST", "OPTIONS"]


class CustomHTTPMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, req: Request, call_next: BaseHTTPMiddleware
    ) -> Response:
        res = await call_next(req)
        res_body = b""
        if "req_body" in context:
            req_body = context["req_body"]
            logger.info(f"Request: url={req.url.path}, body={req_body}")

        if req.path_params:
            logger.info(f"Request: url={req.url.path}, path={req.path_params}")
        if req.query_params:
            logger.info(
                f"Request: url={req.url.path}, query={req.query_params}")

        async for chunk in res.body_iterator:
            res_body += chunk

        if req.url.path != "/api/health/check":
            logger.info(
                f"Status: {res.status_code}, Response: {res_body.decode('utf-8')}")

        return Response(
            content=res_body,
            status_code=res.status_code,
            headers=dict(res.headers),
            media_type=res.media_type
        )


class Middleware:
    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.register()

    def register(self) -> None:
        self.app.add_middleware(CORSMiddleware,
                                allow_origins=origins,
                                allow_methods=methods,
                                allow_headers=["*"],
                                )
        self.app.add_middleware(CustomHTTPMiddleware)
        self.app.add_middleware(ContextMiddleware)
