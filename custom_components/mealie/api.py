from typing import Any, Callable, Mapping, Optional, TypeVar

from custom_components.mealie.model.model import StatisticsResponse

from .exception import (
    ApiException,
    HttpException,
    InternalClientException,
    ParseException,
)
from .http_client import HttpClient
from .model.model import (
    MealPlanResponse,
    RecipeResponse,
    Response,
    Status,
    TokenResponse,
    UserResponse,
)
from .token_repository import TokenRepository

T = TypeVar("T")


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
        except KeyError as error:
            raise ParseException() from error

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

        except HttpException as error:
            raise InternalClientException() from error

        token_reponse = self._parse(
            response=response, parser=TokenResponse.from_json
        )

        await self._token_repository.set_token(token=token_reponse.access_token)
        return token_reponse

    async def get_refresh_token(self) -> TokenResponse:
        url = self._url("/api/auth/refresh")
        headers = self._headers | await self._get_authorization_header()

        try:
            response = await self._http_client.get(url=url, headers=headers)
        except HttpException as error:
            raise InternalClientException() from error

        token_reponse = self._parse(
            response=response, parser=TokenResponse.from_json
        )
        await self._token_repository.set_token(token=token_reponse.access_token)
        return token_reponse

    async def get_meal_plan_this_week(self) -> Optional[MealPlanResponse]:
        url = self._url("/api/meal-plans/this-week")
        headers = self._headers | await self._get_authorization_header()

        meal_plan_response = await self._http_client.get(
            url=url, headers=headers
        )

        if meal_plan_response.data:
            return self._parse(
                response=meal_plan_response, parser=MealPlanResponse.from_json
            )
        else:
            return None

    async def get_user(self) -> UserResponse:
        url = self._url("/api/users/self")
        headers = self._headers | await self._get_authorization_header()

        user_response = await self._http_client.get(url=url, headers=headers)
        return self._parse(
            response=user_response, parser=UserResponse.from_json
        )

    async def get_statistics(self) -> StatisticsResponse:
        url = self._url("/api/debug/statistics")
        headers = self._headers | await self._get_authorization_header()

        statistics_response = await self._http_client.get(
            url=url, headers=headers
        )
        return self._parse(
            response=statistics_response, parser=StatisticsResponse.from_json
        )

    async def get_recipe_today(self) -> Optional[RecipeResponse]:
        url = self._url("/api/meal-plans/today")

        headers = self._headers | await self._get_authorization_header()

        recipe_response = await self._http_client.get(url=url, headers=headers)

        if recipe_response.data:
            return self._parse(
                response=recipe_response, parser=RecipeResponse.from_json
            )
        else:
            return None
