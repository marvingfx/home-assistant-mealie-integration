from dataclasses import dataclass
from typing import Final, Tuple

from homeassistant.components.sensor import SensorEntityDescription

DOMAIN: Final[str] = "mealie"
CONF_API: Final[str] = "api"
CONF_COORDINATOR: Final[str] = "coordinator"

SENSOR_NO_RECIPES_KEY: Final[str] = "total_recipes"
SENSOR_NO_RECIPES_NAME: Final[str] = "Total number of recipes"

SENSOR_NO_UNCATEGORIZED_RECIPES_KEY: Final[str] = "uncategorized_recipes"
SENSOR_NO_UNCATEGORIZED_RECIPES_NAME: Final[str] = "Number of uncategorized recipes"

SENSOR_NO_UNTAGGED_RECIPES_KEY: Final[str] = "untagged_recipes"
SENSOR_NO_UNTAGGED_RECIPES_NAME: Final[str] = "Number of untagged recipes"

SENSOR_TODAY_RECIPE_KEY: Final[str] = "today_recipe"
SENSOR_TODAY_RECIPE_URL: Final[str] = "today_recipy_url"
SENSOR_TODAY_RECIPE_NAME: Final[str] = "Today's recipe"

SENSOR_MEAL_PLAN_KEY: Final[str] = "meal_plan"
SENSOR_MEAL_PLAN_NAME: Final[str] = "This week's meal plan"


@dataclass
class MealieSensorEnitityDescription(SensorEntityDescription):
    ...


SENSOR_TYPES: Tuple[MealieSensorEnitityDescription, ...] = (
    MealieSensorEnitityDescription(
        key=SENSOR_NO_RECIPES_KEY,
        name=SENSOR_NO_RECIPES_NAME,
        native_unit_of_measurement="recipies",
        icon="mdi:food",
    ),
    MealieSensorEnitityDescription(
        key=SENSOR_NO_UNCATEGORIZED_RECIPES_KEY,
        name=SENSOR_NO_UNCATEGORIZED_RECIPES_NAME,
        native_unit_of_measurement="recipies",
        icon="mdi:food",
    ),
    MealieSensorEnitityDescription(
        key=SENSOR_NO_UNTAGGED_RECIPES_KEY,
        name=SENSOR_NO_UNTAGGED_RECIPES_NAME,
        native_unit_of_measurement="recipies",
        icon="mdi:food",
    ),
)

next_meal_sensor_entitity_description = MealieSensorEnitityDescription(
    key=SENSOR_TODAY_RECIPE_KEY,
    name=SENSOR_TODAY_RECIPE_NAME,
    icon="mdi:food",
)

meal_plan_sensor_entity_description = MealieSensorEnitityDescription(
    key=SENSOR_MEAL_PLAN_KEY,
    name=SENSOR_MEAL_PLAN_NAME,
    icon="mdi:food",
)
