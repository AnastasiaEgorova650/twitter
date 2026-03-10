from http import HTTPStatus

from pydantic import BaseModel, ConfigDict, Field


class ResponseSchema(BaseModel):


    result_user: bool = Field(alias="result", default=True)
    model_config = ConfigDict(from_attributes=True)


class ErrorResponseSchema(ResponseSchema):


    result_user: bool = Field(alias="result", default=True)
    error_type: int = HTTPStatus.NOT_FOUND  # 404
    error_message: str = "Not found"


class UnauthorizedResponseSchema(ErrorResponseSchema):


    error_type: int = HTTPStatus.UNAUTHORIZED  # 401
    error_message: str = "User authorization error"


class ValidationResponseSchema(ErrorResponseSchema):


    error_type: int = HTTPStatus.UNPROCESSABLE_ENTITY  # 422
    error_message: str = "Invalid input data"


class LockedResponseSchema(ErrorResponseSchema):


    error_type: int = HTTPStatus.LOCKED  # 423
    error_message: str = "The action is blocked"


class BadResponseSchema(ResponseSchema):


    error_type: int = HTTPStatus.BAD_REQUEST  # 400
    error_message: str = "The image was not attached to the request"
