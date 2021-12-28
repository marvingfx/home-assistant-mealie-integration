from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.core import HomeAssistant
import logging
from datetime import timedelta

from .api import Api


class MealieDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(
        self, hass: HomeAssistant, config_entry: ConfigEntry, mealie_api: Api
    ) -> None:
        self._mealie_api = mealie_api
        logger = logging.getLogger(__name__)
        super().__init__(
            hass=hass,
            logger=logger,
            name="MealieDataUpdateCoordinator",
            update_interval=timedelta(minutes=30),
        )
