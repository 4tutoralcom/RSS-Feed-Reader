from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN
from .rss_feed_parser import fetch_feed_sync

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    feeds = entry.data["feeds"]
    sensors = [RSSFeedSensor(feed_url) for feed_url in feeds]
    async_add_entities(sensors, update_before_add=True)


class RSSFeedSensor(Entity):
    def __init__(self, feed_url):
        self._url = feed_url
        self._attr_name = f"RSS Feed - {self._url}"
        self._state = None
        self._attrs = {}

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attrs
    
    @property
    def should_poll(self) -> bool:
        return True
    
async def async_update(self):
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.debug("This is a debug message")
    entry = await self.hass.async_add_executor_job(fetch_feed_sync, self._url)
    _LOGGER.debug(entry["title"])
    if entry:
        self._state = entry["title"]
        self._attrs = {
            "guid ": entry["guid "],
            "link": entry["link"],
            "published": entry["published"]
        }
