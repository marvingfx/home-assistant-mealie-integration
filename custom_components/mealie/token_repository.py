from typing import Optional

from custom_components.mealie.exception import NoTokenException


class TokenRepository:
    def __init__(self) -> None:
        self._token: Optional[str] = None

    def set_token(self, token: str) -> None:
        self._token = token

    def get_token(self) -> str:
        if self._token:
            return self._token
        else:
            raise NoTokenException()

    def purge_token(self) -> None:
        self._token = None
