from typing import Optional

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.core import HomeAssistant

from .exception import NoTokenException


class TokenRepository:
    def __init__(self) -> None:
        self._token: Optional[str] = None

    async def set_token(self, token: str) -> None:
        self._token = token

    async def get_token(self) -> str:
        if self._token:
            return self._token
        else:
            raise NoTokenException()

    async def purge_token(self) -> None:
        self._token = None


class HomeAssistantTokenRepository(TokenRepository):
    # TODO seperate this class from main mealie api

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self._hass = hass
        self._entry = entry
        super().__init__()

    async def set_token(self, token: str) -> None:
        data = {**self._entry.data, CONF_ACCESS_TOKEN: token}

        self._hass.config_entries.async_update_entry(self._entry, data=data)

    async def get_token(self) -> str:
        return self._entry.data[CONF_ACCESS_TOKEN]

    async def purge_token(self) -> None:
        data = {**self._entry.data, CONF_ACCESS_TOKEN: None}

        self._hass.config_entries.async_update_entry(self._entry, data=data)
