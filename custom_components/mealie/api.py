from typing import Any, Callable, Mapping, TypeVar

from .exception import (
    ApiException,
    HttpException,
    InternalClientException,
    ParseException,
)
from .http_client import HttpClient
from .model.model import (
    MealPlanResponse,
    Response,
    Status,
    TokenResponse,
    UserResponse,
)
from .token_repository import TokenRepository

T = TypeVar("T")

import logging

_LOGGER = logging.getLogger(__name__)


class Api:
    def __init__(
        self,
        http_client: HttpClient,
        base_url: str,
        token_repository: TokenRepository,
    ) -> None:
        self._http_client = http_client
        self._token_repository = token_repository
        self._base_url = base_url
        self._headers = {"accept": "application/json"}

    def _url(self, suffix: str) -> str:
        return f"{self._base_url}{suffix}"

    async def _get_authorization_header(self) -> Mapping[str, str]:
        access_token = await self._token_repository.get_token()
        return {"Authorization": f"Bearer {access_token}"}

    def _parse(
        self, response: Response, parser: Callable[[Mapping[str, Any]], T]
    ) -> T:
        if response.status == Status.FAILURE:
            raise ApiException()
        try:
            return parser(response.data)
        except KeyError:
            raise ParseException()

    async def get_token(
        self, username: str, password: str, long_token: bool = False
    ) -> TokenResponse:
        url = (
            self._url("/api/auth/token/long")
            if long_token
            else self._url("/api/auth/token")
        )
        headers = self._headers

        try:
            response = await self._http_client.post(
                url=url,
                headers=headers,
                data={"username": username, "password": password},
            )

            _LOGGER.info(response)
        except HttpException:
            raise InternalClientException()

        token_reponse = self._parse(
            response=response, parser=TokenResponse.from_json
        )

        _LOGGER.info(token_reponse)
        await self._token_repository.set_token(token=token_reponse.access_token)
        return token_reponse

    async def get_refresh_token(self) -> TokenResponse:
        url = self._url("/api/auth/refresh")
        headers = self._headers | await self._get_authorization_header()

        try:
            response = await self._http_client.get(url=url, headers=headers)
        except HttpException:
            raise InternalClientException()

        token_reponse = self._parse(
            response=response, parser=TokenResponse.from_json
        )
        await self._token_repository.set_token(token=token_reponse.access_token)
        return token_reponse

    async def get_meal_plan_this_week(self) -> MealPlanResponse:
        url = self._url("/api/meal-plans/this-week")
        headers = self._headers | await self._get_authorization_header()

        meal_plan_response = await self._http_client.get(
            url=url, headers=headers
        )
        return self._parse(
            response=meal_plan_response, parser=MealPlanResponse.from_json
        )

    async def get_user(self) -> UserResponse:
        url = self._url("/api/users/self")
        headers = self._headers | await self._get_authorization_header()

        user_response = await self._http_client.get(url=url, headers=headers)
        return self._parse(
            response=user_response, parser=UserResponse.from_json
        )
