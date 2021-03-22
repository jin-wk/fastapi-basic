from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from app.model import ResponseBaseModel
# from app.service.slack import Slack
from core.logger import Logger

logger = Logger().logger
# slack = Slack()


class ExceptionHandler:
    def __init__(self, app: FastAPI) -> None:
        self.app = app
        self.register()

    async def custom_http_exception_handler(
        self, request: Request, exc: HTTPException
    ) -> JSONResponse:
        detail = None
        if isinstance(exc.detail, ResponseBaseModel):
            detail = exc.detail.dict()
            if isinstance(exc.detail.dict()["message"], str):
                detail["message"] = [exc.detail.dict()["message"]]
        content = {
            "status_code": exc.status_code,
            "detail": detail,
        }
        if exc.status_code == 500:
            arr = [
                f"content: {content}",
                f"url: {request.url}",
            ]
            if request.path_params:
                arr.append(f"path: {request.path_params}")
            if request.query_params:
                arr.append(f"query: {request.query_params}")
            # await slack.send("\n".join(arr))
            logger.exception(f"{content}")
        return JSONResponse(status_code=exc.status_code, content=detail)

    async def validation_exception_handler(
        self, request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        content = {
            "code": 1000,
            "message": list(map(lambda x: "{}".format(x['msg']), exc.errors())),
        }
        logger.error(f"{content}")
        return JSONResponse(status_code=400, content=content)

    def register(self) -> None:
        self.app.add_exception_handler(
            HTTPException, self.custom_http_exception_handler)
        self.app.add_exception_handler(
            RequestValidationError, self.validation_exception_handler)
