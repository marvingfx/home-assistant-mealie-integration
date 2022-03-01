import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from custom_components.mealie.api import Api
from custom_components.mealie.const import CONF_API, CONF_COORDINATOR, DOMAIN
from custom_components.mealie.coordinator import MealieDataUpdateCoordinator
from custom_components.mealie.http_client import HttpClient
from custom_components.mealie.token_repository import HomeAssistantTokenRepository

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    client_session = async_get_clientsession(hass=hass)
    http_client = HttpClient(client_session=client_session)
    home_assistant_token_repository = HomeAssistantTokenRepository(
        hass=hass, entry=entry
    )
    await home_assistant_token_repository.set_token(entry.data[CONF_ACCESS_TOKEN])

    base_url = entry.data[CONF_HOST]
    mealie_api = Api(
        http_client=http_client,
        base_url=base_url,
        token_repository=home_assistant_token_repository,
    )

    mealie_coordinator = MealieDataUpdateCoordinator(
        hass=hass, config_entry=entry, mealie_api=mealie_api
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        CONF_API: mealie_coordinator,
        CONF_COORDINATOR: mealie_coordinator,
    }

    await mealie_coordinator.async_config_entry_first_refresh()

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry=entry, platforms=PLATFORMS
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
