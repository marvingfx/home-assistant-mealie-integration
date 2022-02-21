from __future__ import annotations

from datetime import date, datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import CONF_HOST

from typing import Mapping

from custom_components.mealie.model.model import (
    MealPlanResponse,
    RecipeResponse,
)

from .api import Api
from .const import (
    CONF_API,
    CONF_COORDINATOR,
    DOMAIN,
    SENSOR_TYPES,
    MealieSensorEnitityDescription,
    next_meal_sensor_entitity_description,
    meal_plan_sensor_entity_description,
)
from .coordinator import MealieDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry_config: ConfigEntry,
    add_entitities_callback: AddEntitiesCallback,
) -> None:
    mealie_api = hass.data[DOMAIN][entry_config.entry_id][CONF_API]
    mealie_coordinator = hass.data[DOMAIN][entry_config.entry_id][
        CONF_COORDINATOR
    ]

    add_entitities_callback(
        MealieSensor(
            mealie_api=mealie_api,
            mealie_coordinator=mealie_coordinator,
            description=description,
        )
        for description in SENSOR_TYPES
    )

    add_entitities_callback(
        [
            MealieNextmealSensor(
                mealie_api=mealie_api,
                mealie_coordinator=mealie_coordinator,
                description=next_meal_sensor_entitity_description,
            ),
            MealieMealPlanSensor(
                mealie_api=mealie_api,
                mealie_coordinator=mealie_coordinator,
                description=meal_plan_sensor_entity_description,
            ),
        ]
    )

    return True


class MealieSensor(SensorEntity, CoordinatorEntity):
    def __init__(
        self,
        mealie_api: Api,
        mealie_coordinator: MealieDataUpdateCoordinator,
        description: MealieSensorEnitityDescription,
    ) -> None:
        super().__init__(coordinator=mealie_coordinator)
        self._mealie_api = mealie_api
        self.entity_description = description
        self.entity_id = f"sensor.mealie_{description.key}"

    @property
    def native_value(self) -> StateType | date | datetime:
        return (
            self.coordinator.data.get(self.entity_description.key)
            if self.coordinator.data
            else None
        )


class MealieMealPlanSensor(SensorEntity, CoordinatorEntity):
    def __init__(
        self,
        mealie_api: Api,
        mealie_coordinator: MealieDataUpdateCoordinator,
        description: MealieSensorEnitityDescription,
    ) -> None:
        super().__init__(coordinator=mealie_coordinator)
        self._mealie_api = mealie_api
        self.entity_description = description
        self.entity_id = f"sensor.mealie_{description.key}"

    @property
    def native_value(self) -> StateType | date | datetime:
        meal_plan_response: MealPlanResponse = (
            self.coordinator.data.get(self.entity_description.key)
            if self.coordinator.data
            else None
        )

        return meal_plan_response.group if meal_plan_response else None

    @property
    def extra_state_attributes(self) -> Mapping[str, str]:
        meal_plan_response: MealPlanResponse = (
            self.coordinator.data.get(self.entity_description.key)
            if self.coordinator.data
            else None
        )

        return {
            "start_date": datetime.combine(
                meal_plan_response.start_date, datetime.min.time()
            )
            if meal_plan_response
            else None,
            "end_date": datetime.combine(
                meal_plan_response.end_date, datetime.max.time()
            )
            if meal_plan_response
            else None,
        }


class MealieNextmealSensor(SensorEntity, CoordinatorEntity):
    def __init__(
        self,
        mealie_api: Api,
        mealie_coordinator: MealieDataUpdateCoordinator,
        description: MealieSensorEnitityDescription,
    ) -> None:
        super().__init__(coordinator=mealie_coordinator)
        self._mealie_api = mealie_api
        self.entity_description = description
        self.entity_id = f"sensor.mealie_{description.key}"

    @property
    def native_value(self) -> StateType | date | datetime:
        recipe_response = (
            self.coordinator.data.get(self.entity_description.key)
            if self.coordinator.data
            else None
        )

        return recipe_response.name if recipe_response else None

    @property
    def extra_state_attributes(self) -> Mapping[str, str]:
        recipe_response: RecipeResponse = (
            self.coordinator.data.get(self.entity_description.key)
            if self.coordinator.data
            else None
        )

        slug = recipe_response.slug if recipe_response else None
        host = self.coordinator.config_entry.data.get(CONF_HOST)

        return {"url": f"{host}/recipe/{slug}" if slug and host else None}
