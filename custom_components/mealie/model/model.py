from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum, auto
from typing import Any, List, Mapping, Optional


def parse_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()


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


@dataclass(frozen=True)
class MealPlanResponse:
    group: str
    start_date: date
    end_date: date
    plan_days: List[PlanDay]
    uid: int
    shopping_list: int

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> MealPlanResponse:
        return MealPlanResponse(
            group=json_data["group"],
            start_date=parse_date(json_data["startDate"]),
            end_date=parse_date(json_data["endDate"]),
            plan_days=[
                PlanDay.from_json(json_data=plan_day)
                for plan_day in json_data.get("planDays", list())
            ],
            uid=json_data["uid"],
            shopping_list=json_data["shoppingList"],
        )


@dataclass(frozen=True)
class PlanDay:
    date: date
    meals: List[Meal]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> PlanDay:
        return PlanDay(
            date=parse_date(json_data["date"]),
            meals=[
                Meal.from_json(json_data=meal)
                for meal in json_data.get("meals", list())
            ],
        )


@dataclass(frozen=True)
class Meal:
    slug: Optional[str]
    name: Optional[str]
    description: Optional[str]

    @classmethod
    def from_json(cls, json_data: Mapping[str, Any]) -> Meal:
        return Meal(
            slug=json_data.get("slug"),
            name=json_data.get("name"),
            description=json_data.get("description"),
        )
