from typing import Final, Tuple

from homeassistant.components.sensor import SensorEntityDescription
from dataclasses import dataclass


DOMAIN: Final = "mealie"
CONF_API: Final = "api"
CONF_COORDINATOR: Final = "coordinator"

SENSOR_NAME_KEY: Final = "name"
SENSOR_NAME_NAME: Final = "Name"

SENSOR_NO_RECIPES_KEY: Final = "total_recipes"
SENSOR_NO_RECIPES_NAME: Final = "Total number of recipes"

SENSOR_NO_UNCATEGORIZED_RECIPES_KEY: Final = "uncategorized_recipes"
SENSOR_NO_UNCATEGORIZED_RECIPES_NAME: Final = "Number of uncategorized recipes"

SENSOR_NO_UNTAGGED_RECIPES_KEY: Final = "untagged_recipes"
SENSOR_NO_UNTAGGED_RECIPES_NAME: Final = "Number of untagged recipes"


@dataclass
class MealieSensorEnitityDescription(SensorEntityDescription):
    entity_registry_enabled_default: bool = False


SENSOR_TYPES: Tuple[MealieSensorEnitityDescription, ...] = (
    MealieSensorEnitityDescription(
        key=SENSOR_NAME_KEY,
        name=SENSOR_NAME_NAME,
        native_unit_of_measurement="Name",
        icon="mdi:account",
    ),
    MealieSensorEnitityDescription(
        key=SENSOR_NO_RECIPES_KEY,
        name=SENSOR_NO_RECIPES_NAME,
        native_unit_of_measurement="int",
        icon="mdi:account",
    ),
    MealieSensorEnitityDescription(
        key=SENSOR_NO_UNCATEGORIZED_RECIPES_KEY,
        name=SENSOR_NO_UNCATEGORIZED_RECIPES_NAME,
        native_unit_of_measurement="int",
        icon="mdi:account",
    ),
    MealieSensorEnitityDescription(
        key=SENSOR_NO_UNTAGGED_RECIPES_KEY,
        name=SENSOR_NO_UNTAGGED_RECIPES_NAME,
        native_unit_of_measurement="int",
        icon="mdi:account",
    ),
)
