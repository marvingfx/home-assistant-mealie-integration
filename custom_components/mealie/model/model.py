from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, List, Mapping, Optional


@dataclass(frozen=True)
class BaseResponse:
    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> BaseResponse:
        pass


@dataclass(frozen=True)
class TokenResponse(BaseResponse):
    access_token: str
    token_type: str

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> TokenResponse:
        return TokenResponse(
            access_token=json_data["access_token"],
            token_type=json_data["token_type"],
        )


@dataclass(frozen=True)
class ErrorResponse(BaseResponse):
    detail: List[Detail]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> ErrorResponse:
        return ErrorResponse(
            detail=[
                Detail.from_json(json_data=detail)
                for detail in json_data.get("detail", list())
            ]
        )


@dataclass(frozen=True)
class Detail:
    loc: List[str]
    msg: Optional[str]
    type: Optional[str]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> Detail:
        return Detail(
            loc=[str(entry) for entry in json_data.get("loc", list())],
            msg=json_data.get("msg"),
            type=json_data.get("type"),
        )


class Status(Enum):
    SUCCESS = auto()
    FAILURE = auto()


@dataclass(frozen=True)
class Response:
    status: Status
    status_code: int
    data: Mapping[str, Any]
