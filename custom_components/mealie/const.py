from dataclasses import dataclass
from typing import Final, Tuple

from homeassistant.components.sensor import SensorEntityDescription

DOMAIN: Final = "mealie"
CONF_API: Final = "api"
CONF_COORDINATOR: Final = "coordinator"

SENSOR_NO_RECIPES_KEY: Final = "total_recipes"
SENSOR_NO_RECIPES_NAME: Final = "Total number of recipes"

SENSOR_NO_UNCATEGORIZED_RECIPES_KEY: Final = "uncategorized_recipes"
SENSOR_NO_UNCATEGORIZED_RECIPES_NAME: Final = "Number of uncategorized recipes"

SENSOR_NO_UNTAGGED_RECIPES_KEY: Final = "untagged_recipes"
SENSOR_NO_UNTAGGED_RECIPES_NAME: Final = "Number of untagged recipes"

SENSOR_TODAY_RECIPE_KEY: Final = "today_recipe"
SENSOR_TODAY_RECIPE_NAME: Final = "Today's recipe"

SENSOR_MONDAY_RECIPE_KEY: Final = "monday_recipe"
SENSOR_MONDAY_RECIPE_NAME: Final = "Monday's recipe"
SENSOR_TUESDAY_RECIPE_KEY: Final = "tuesday_recipe"
SENSOR_TUESDAY_RECIPE_NAME: Final = "Tuesday's recipe"
SENSOR_WEDNESDAY_RECIPE_KEY: Final = "wednesday_recipe"
SENSOR_WEDNESDAY_RECIPE_NAME: Final = "Wednesday's recipe"
SENSOR_THURSDAY_RECIPE_KEY: Final = "thursday_recipe"
SENSOR_THURSDAY_RECIPE_NAME: Final = "Thursday's recipe"
SENSOR_FRIDAY_RECIPE_KEY: Final = "friday_recipe"
SENSOR_FRIDAY_RECIPE_NAME: Final = "Friday's recipe"
SENSOR_SATURDAY_RECIPE_KEY: Final = "saturday_recipe"
SENSOR_SATURDAY_RECIPE_NAME: Final = "Saturday's recipe"
SENSOR_SUNDAY_RECIPE_KEY: Final = "sunday_recipe"
SENSOR_SUNDAY_RECIPE_NAME: Final = "Sunday's recipe"


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
    MealieSensorEnitityDescription(
        key=SENSOR_TODAY_RECIPE_KEY,
        name=SENSOR_TODAY_RECIPE_NAME,
        icon="mdi:food",
    ),
    MealieSensorEnitityDescription(
        key=SENSOR_MONDAY_RECIPE_KEY,
        name=SENSOR_MONDAY_RECIPE_NAME,
        icon="mdi:food",
    ),
    MealieSensorEnitityDescription(
        key=SENSOR_TUESDAY_RECIPE_KEY,
        name=SENSOR_TUESDAY_RECIPE_NAME,
        icon="mdi:food",
    ),
    MealieSensorEnitityDescription(
        key=SENSOR_WEDNESDAY_RECIPE_KEY,
        name=SENSOR_WEDNESDAY_RECIPE_NAME,
        icon="mdi:food",
    ),
    MealieSensorEnitityDescription(
        key=SENSOR_THURSDAY_RECIPE_KEY,
        name=SENSOR_THURSDAY_RECIPE_NAME,
        icon="mdi:food",
    ),
    MealieSensorEnitityDescription(
        key=SENSOR_FRIDAY_RECIPE_KEY,
        name=SENSOR_FRIDAY_RECIPE_NAME,
        icon="mdi:food",
    ),
    MealieSensorEnitityDescription(
        key=SENSOR_SATURDAY_RECIPE_KEY,
        name=SENSOR_SATURDAY_RECIPE_NAME,
        icon="mdi:food",
    ),
    MealieSensorEnitityDescription(
        key=SENSOR_SUNDAY_RECIPE_KEY,
        name=SENSOR_SUNDAY_RECIPE_NAME,
        icon="mdi:food",
    ),
)
