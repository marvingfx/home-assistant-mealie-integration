from typing import Union

import pytest
from pytest_mock import MockerFixture

from custom_components.mealie.api import Api, ApiException, ParseException
from custom_components.mealie.client import HttpClient
from custom_components.mealie.exception import InternalClientException
from custom_components.mealie.model.model import Response, Status, TokenResponse

success_response = Response(
    status=Status.SUCCESS,
    status_code=200,
    data={
        "access_token": "random_token_here",
        "token_type": "bearer",
    },
)

success_expected = TokenResponse(
    access_token="random_token_here", token_type="bearer"
)

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
    response: Response, expected: TokenResponse, mocker: MockerFixture
):
    mocker.patch(
        "custom_components.mealie.client.HttpClient.post", return_value=response
    )

    async with HttpClient() as http_client:
        api = Api(http_client=http_client, base_url="")
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
):
    mocker.patch(
        "custom_components.mealie.client.HttpClient.post", return_value=response
    )

    with pytest.raises(expected):  # type: ignore
        async with HttpClient() as http_client:
            api = Api(http_client=http_client, base_url="")
            _ = await api.get_token(username="", password="", long_token=False)
