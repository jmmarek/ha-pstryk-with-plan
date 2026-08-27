"""The Pstryk with plan integration."""

from .api import PstrykApi
from .const import CONF_API_KEY, DOMAIN
from .coordinator import PstrykCoordinator

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, SupportsResponse

_PLATFORMS: list[Platform] = [Platform.SENSOR]

type PstrykConfigEntry = ConfigEntry[PstrykCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: PstrykConfigEntry) -> bool:
    """Set up Pstryk with plan from a config entry."""

    api = PstrykApi(api_key=entry.data[CONF_API_KEY])

    coordinator = PstrykCoordinator(
        hass,
        api,
    )

    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        _PLATFORMS,
    )


    return True


async def async_unload_entry(hass: HomeAssistant, entry: PstrykConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
