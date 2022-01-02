from homeassistant.config_entries import ConfigEntry
from typing import Any
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from homeassistant.core import HomeAssistant
import logging
from datetime import timedelta

from custom_components.mealie.const import (
    SENSOR_NAME_KEY,
    SENSOR_NO_RECIPES_KEY,
    SENSOR_NO_UNCATEGORIZED_RECIPES_KEY,
    SENSOR_NO_UNTAGGED_RECIPES_KEY,
)

from .api import Api

DATA_MEAL_PLAN = "data_meal_plan"
DATA_USER = "data_user"


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
            meal_plan_response = (
                await self._mealie_api.get_meal_plan_this_week()
            )
            current_user_response = await self._mealie_api.get_user()
            statistics_response = await self._mealie_api.get_statistics()

            return {
                DATA_MEAL_PLAN: meal_plan_response,
                DATA_USER: current_user_response,
                SENSOR_NAME_KEY: current_user_response.full_name,
                SENSOR_NO_RECIPES_KEY: statistics_response.total_recipes,
                SENSOR_NO_UNCATEGORIZED_RECIPES_KEY: statistics_response.uncategorized_recipes,
                SENSOR_NO_UNTAGGED_RECIPES_KEY: statistics_response.untagged_recipes,
            }

        except Exception as error:
            self.logger.error(error)
            raise UpdateFailed() from error