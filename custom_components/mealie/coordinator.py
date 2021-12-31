from homeassistant.config_entries import ConfigEntry
from typing import Any
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
        self._entry = config_entry
        logger = logging.getLogger(__name__)
        super().__init__(
            hass=hass,
            logger=logger,
            name="MealieDataUpdateCoordinator",
            update_interval=timedelta(minutes=30),
        )

    async def _async_update_data(self) -> Any:
        return await super()._async_update_data()
        # TODO implement function
