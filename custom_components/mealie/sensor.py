from __future__ import annotations

from datetime import date, datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import Api
from .const import (
    CONF_API,
    CONF_COORDINATOR,
    DOMAIN,
    SENSOR_TYPES,
    MealieSensorEnitityDescription,
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
        # self.entity_id = f"sensor.mealie.{description.key}"

    @property
    def native_value(self) -> StateType | date | datetime:
        return (
            self.coordinator.data.get(self.entity_description.key)
            if self.coordinator.data
            else None
        )
