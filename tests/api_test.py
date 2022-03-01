from datetime import date
from typing import Union

from aiohttp.client import ClientSession
import pytest
from pytest_mock import MockerFixture

from custom_components.mealie.api import Api, ApiException, ParseException
from custom_components.mealie.exception import InternalClientException
from custom_components.mealie.http_client import HttpClient
from custom_components.mealie.model.model import (
    Meal,
    MealPlanResponse,
    PlanDay,
    Response,
    Status,
    TokenResponse,
)
from custom_components.mealie.token_repository import TokenRepository


@pytest.fixture(scope="function")
async def http_client(loop) -> HttpClient:
    yield HttpClient(client_session=ClientSession())


success_response = Response(
    status=Status.SUCCESS,
    status_code=200,
    data={
        "access_token": "random_token_here",
        "token_type": "bearer",
    },
)

success_expected = TokenResponse(access_token="random_token_here", token_type="bearer")

invalid_response = Response(
    status=Status.SUCCESS,
    status_code=200,
    data={
        "access_taoken": "random_token_here",
        "token_thype": "bearer",
    },
)

invalid_expected = ParseException

error_response = Response(
    status=Status.FAILURE,
    status_code=400,
    data={"detail": {"msg": "something went wrong"}},
)

error_expected = ApiException


@pytest.mark.parametrize(
    ("response", "expected"), ([(success_response, success_expected)])
)
async def test_valid_response(
    response: Response,
    expected: TokenResponse,
    mocker: MockerFixture,
    http_client: HttpClient,
) -> None:
    mocker.patch(
        "custom_components.mealie.http_client.HttpClient.post",
        return_value=response,
    )

    api = Api(
        http_client=http_client,
        base_url="",
        token_repository=TokenRepository(),
    )
    actual = await api.get_token(username="", password="", long_token=False)
    assert actual == expected


@pytest.mark.parametrize(
    ("response", "expected"),
    zip([invalid_response, error_response], [invalid_expected, error_expected]),
)
async def test_invalid_response(
    response: Response,
    expected: Union[ApiException, InternalClientException, ParseException],
    mocker: MockerFixture,
    http_client: HttpClient,
) -> None:
    mocker.patch(
        "custom_components.mealie.http_client.HttpClient.post",
        return_value=response,
    )

    with pytest.raises(expected):  # type: ignore
        api = Api(
            http_client=http_client,
            base_url="",
            token_repository=TokenRepository(),
        )
        _ = await api.get_token(username="", password="", long_token=False)


async def test_get_token(
    mocker: MockerFixture,
    http_client: HttpClient,
) -> None:
    mocker.patch(
        "custom_components.mealie.http_client.HttpClient.post",
        return_value=success_response,
    )

    api = Api(
        http_client=http_client,
        base_url="",
        token_repository=TokenRepository(),
    )
    token_response = await api.get_token(username="", password="", long_token=False)
    assert token_response == TokenResponse(
        access_token="random_token_here", token_type="bearer"
    )

    assert await api._get_authorization_header() == {
        "Authorization": "Bearer random_token_here"
    }


async def test_get_meal_plan_this_week(
    mocker: MockerFixture, http_client: HttpClient
) -> None:
    mocker.patch(
        "custom_components.mealie.token_repository.TokenRepository.get_token",
        return_value="random_token_here",
    )

    mocker.patch(
        "custom_components.mealie.http_client.HttpClient.get",
        return_value=Response(
            status=Status.SUCCESS,
            status_code=200,
            data={
                "group": "Test",
                "startDate": "2021-11-29",
                "endDate": "2021-12-03",
                "planDays": [
                    {
                        "date": "2021-11-29",
                        "meals": [
                            {
                                "slug": "meal1",
                                "name": "meal1",
                                "description": "meal1 description",
                            },
                            {
                                "slug": None,
                                "name": "meal2",
                                "description": "meal2 description",
                            },
                            {
                                "slug": None,
                                "name": "meal3",
                                "description": None,
                            },
                        ],
                    },
                    {
                        "date": "2021-11-30",
                        "meals": [
                            {
                                "slug": "meal1",
                                "name": "meal1",
                                "description": "meal1 description",
                            },
                        ],
                    },
                    {
                        "date": "2021-12-01",
                        "meals": [
                            {
                                "slug": "meal1",
                                "name": "meal1",
                                "description": "meal1 description",
                            },
                        ],
                    },
                    {
                        "date": "2021-12-02",
                        "meals": [
                            {
                                "slug": "meal1",
                                "name": "meal1",
                                "description": "meal1 description",
                            },
                        ],
                    },
                    {
                        "date": "2021-12-03",
                        "meals": [
                            {
                                "slug": "meal1",
                                "name": "meal1",
                                "description": "meal1 description",
                            },
                        ],
                    },
                ],
                "uid": 27,
                "shoppingList": 25,
            },
        ),
    )

    api = Api(
        http_client=http_client,
        base_url="",
        token_repository=TokenRepository(),
    )
    meal_plan_response = await api.get_meal_plan_this_week()
    assert meal_plan_response == MealPlanResponse(
        group="Test",
        start_date=date(2021, 11, 29),
        end_date=date(2021, 12, 3),
        plan_days=[
            PlanDay(
                date=date(2021, 11, 29),
                meals=[
                    Meal(
                        slug="meal1",
                        name="meal1",
                        description="meal1 description",
                    ),
                    Meal(
                        slug=None,
                        name="meal2",
                        description="meal2 description",
                    ),
                    Meal(slug=None, name="meal3", description=None),
                ],
            ),
            PlanDay(
                date=date(2021, 11, 30),
                meals=[
                    Meal(
                        slug="meal1",
                        name="meal1",
                        description="meal1 description",
                    )
                ],
            ),
            PlanDay(
                date=date(2021, 12, 1),
                meals=[
                    Meal(
                        slug="meal1",
                        name="meal1",
                        description="meal1 description",
                    )
                ],
            ),
            PlanDay(
                date=date(2021, 12, 2),
                meals=[
                    Meal(
                        slug="meal1",
                        name="meal1",
                        description="meal1 description",
                    )
                ],
            ),
            PlanDay(
                date=date(2021, 12, 3),
                meals=[
                    Meal(
                        slug="meal1",
                        name="meal1",
                        description="meal1 description",
                    )
                ],
            ),
        ],
        uid=27,
        shopping_list=25,
    )
