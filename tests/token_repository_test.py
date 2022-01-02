import pytest

from custom_components.mealie.exception import NoTokenException
from custom_components.mealie.token_repository import TokenRepository


@pytest.fixture(scope="function")
async def token_repository(loop) -> TokenRepository:
    token_repository = TokenRepository()
    await token_repository.set_token("random_token_here")
    return token_repository


async def test_set_get_token(token_repository: TokenRepository) -> None:
    assert await token_repository.get_token() == "random_token_here"
    await token_repository.set_token(token="random_new_token_here")
    assert await token_repository.get_token() == "random_new_token_here"


async def test_purge_token(token_repository: TokenRepository) -> None:
    assert await token_repository.get_token() == "random_token_here"
    await token_repository.purge_token()

    with pytest.raises(NoTokenException):
        await token_repository.get_token()
