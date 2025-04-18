from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

DOMAIN = "rss_reader"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = entry.data

    # ✅ Correctly await forward setup
    await hass.config_entries.async_forward_entry_setup(entry, "sensor")

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
