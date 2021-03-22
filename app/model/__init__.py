from pydantic import BaseModel


class ResponseBaseModel(BaseModel):
    code: int
    message: str


class ResponseErrModel(ResponseBaseModel):
    code: int = 2000


class ResponseExcModel(ResponseBaseModel):
    code: int = 3000
