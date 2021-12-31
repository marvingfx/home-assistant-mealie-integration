from typing import Tuple
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import (
    CONF_ACCESS_TOKEN,
    CONF_HOST,
    CONF_PASSWORD,
    CONF_USERNAME,
)
from .http_client import HttpClient

from .model.model import TokenResponse, UserResponse

from .token_repository import TokenRepository
from .api import Api
from .const import DOMAIN
import voluptuous as vol
import logging
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)


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


class MealieConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        _LOGGER.info("start of async_step_user")
        if (
            user_input
            and user_input.get(CONF_USERNAME) is not None
            and user_input.get(CONF_PASSWORD) is not None
            and user_input.get(CONF_HOST) is not None
        ):
            try:
                _LOGGER.info("Authenticating")
                token_response, user_response = await MealieHelper.authenticate(
                    hass=self.hass,
                    username=user_input[CONF_USERNAME],
                    password=user_input[CONF_PASSWORD],
                    host=user_input[CONF_HOST],
                )

                await self.async_set_unique_id(user_response.id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_response.full_name,
                    data={
                        CONF_ACCESS_TOKEN: token_response.access_token,
                        CONF_HOST: user_input[CONF_HOST],
                    },
                )
            except:
                _LOGGER.exception("Something went wrong")
        else:
            _LOGGER.info("show form")
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required(CONF_USERNAME): str,
                        vol.Required(CONF_PASSWORD): str,
                        vol.Required(CONF_HOST): str,
                    }
                ),
            )
