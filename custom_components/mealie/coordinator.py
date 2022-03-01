from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from custom_components.mealie.exception import ApiException, ParseException

from .api import Api
from .const import (
    SENSOR_MEAL_PLAN_KEY,
    SENSOR_NO_RECIPES_KEY,
    SENSOR_NO_UNCATEGORIZED_RECIPES_KEY,
    SENSOR_NO_UNTAGGED_RECIPES_KEY,
    SENSOR_TODAY_RECIPE_KEY,
)


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
        try:
            await self._mealie_api.get_refresh_token()
        except (ApiException, ParseException) as error:
            raise ConfigEntryAuthFailed() from error

        try:
            statistics_response = await self._mealie_api.get_statistics()
            next_recipe_response = await self._mealie_api.get_recipe_today()
            meal_plan_response = await self._mealie_api.get_meal_plan_this_week()

            return {
                SENSOR_MEAL_PLAN_KEY: meal_plan_response,
                SENSOR_TODAY_RECIPE_KEY: next_recipe_response,
                SENSOR_NO_RECIPES_KEY: statistics_response.total_recipes,
                SENSOR_NO_UNCATEGORIZED_RECIPES_KEY: statistics_response.uncategorized_recipes,
                SENSOR_NO_UNTAGGED_RECIPES_KEY: statistics_response.untagged_recipes,
            }

        except (ApiException, ParseException) as error:
            self.logger.error(error)
            raise UpdateFailed() from error
