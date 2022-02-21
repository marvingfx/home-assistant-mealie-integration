import logging
from typing import Tuple

import voluptuous as vol
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import IntegrationError
from homeassistant.helpers import config_entry_oauth2_flow
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import Api
from .const import DOMAIN
from .http_client import HttpClient
from .model.model import TokenResponse, UserResponse
from .token_repository import TokenRepository


class MealieHelper:
    """something here"""

    @staticmethod
    async def authenticate(
        hass: HomeAssistant, username: str, password: str, host: str
    ) -> Tuple[TokenResponse, UserResponse]:
        client_session = async_get_clientsession(hass=hass)
        http_client = HttpClient(client_session=client_session)
        api = Api(
            http_client=http_client,
            base_url=host,
            token_repository=TokenRepository(),
        )

        token_response = await api.get_token(
            username=username, password=password
        )
        user_response = await api.get_user()

        return (token_response, user_response)


class MealieConfigFlow(
    config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN
):
    def __init__(self) -> None:
        super().__init__()
        self.host = None
        self.username = None

    DOMAIN = DOMAIN

    @property
    def logger(self) -> logging.Logger:
        """Return logger."""
        return logging.getLogger(__name__)

    async def async_step_user(self, user_input=None):
        self.logger.info("start of async_step_user")
        if (
            user_input
            and user_input.get(CONF_USERNAME) is not None
            and user_input.get(CONF_PASSWORD) is not None
            and user_input.get(CONF_HOST) is not None
        ):
            try:
                username = user_input[CONF_USERNAME]
                password = user_input[CONF_PASSWORD]
                host = user_input[CONF_HOST]

                token_response, user_response = await MealieHelper.authenticate(
                    hass=self.hass,
                    username=username,
                    password=password,
                    host=host,
                )

                config_entry = await self.async_set_unique_id(user_response.id)
                data = {
                    CONF_USERNAME: username,
                    CONF_ACCESS_TOKEN: token_response.access_token,
                    CONF_HOST: host,
                }

                if config_entry:
                    self.hass.config_entries.async_update_entry(
                        config_entry, data=data
                    )
                    await self.hass.config_entries.async_reload(
                        config_entry.entry_id
                    )
                    return self.async_abort(reason="Reauth succesful")

                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_response.full_name,
                    data=data,
                )
            except Exception as error:
                raise IntegrationError("Could not setup integration") from error
        else:
            self.logger.info("show form")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_HOST, default=self.host): str,
                        vol.Required(CONF_USERNAME, default=self.username): str,
                        vol.Required(CONF_PASSWORD): str,
                    }
                ),
            )

    async def async_step_reauth(self, user_input=None):
        self.host = user_input.get(CONF_HOST)
        self.username = user_input.get(CONF_USERNAME)

        return await self.async_step_user()
