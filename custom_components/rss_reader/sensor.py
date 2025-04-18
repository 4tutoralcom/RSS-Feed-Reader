import logging
from homeassistant.helpers.entity import Entity
from .rss_feed_parser import fetch_feed_sync
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    feeds = config_entry.data.get("feeds", [])
    sensors = [RSSFeedSensor(url) for url in feeds]
    async_add_entities(sensors, True)

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

async def async_update(self):
    _LOGGER = logging.getLogger(__name__)
    _LOGGER.debug("This is a debug message")
    entry = await self.hass.async_add_executor_job(fetch_feed_sync, self._url)
    if entry:
        self._state = entry["title"]
        self._attrs = {
            "summary": entry["summary"],
            "link": entry["link"],
            "published": entry["published"]
        }
