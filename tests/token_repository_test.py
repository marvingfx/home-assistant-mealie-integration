import pytest

from custom_components.mealie.exception import NoTokenException
from custom_components.mealie.token_repository import TokenRepository


@pytest.fixture(scope="function")
def token_repository() -> TokenRepository:
    token_repository = TokenRepository()
    token_repository.set_token("random_token_here")
    return token_repository


def test_set_get_token(token_repository: TokenRepository) -> None:
    assert token_repository.get_token() == "random_token_here"
    token_repository.set_token(token="random_new_token_here")
    assert token_repository.get_token() == "random_new_token_here"


def test_purge_token(token_repository: TokenRepository) -> None:
    assert token_repository.get_token() == "random_token_here"
    token_repository.purge_token()

    with pytest.raises(NoTokenException):
        token_repository.get_token()
