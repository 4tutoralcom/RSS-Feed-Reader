import logging
import feedparser

from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
from homeassistant.util import slugify

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    feeds = entry.data["feeds"]
    sensors = [RSSFeedSensor(feed_url) for feed_url in feeds]
    async_add_entities(sensors, update_before_add=True)

class RSSFeedSensor(SensorEntity):
    def __init__(self, feed_url):
        self._url = feed_url
        self._state = None
        self._attr_name = f"RSS Feed: {feed_url}"
        self._attr_unique_id = f"rss_feed_{slugify(feed_url)}"
        self._attr_extra_state_attributes = {}

    @property
    def native_value(self):
        return self._state

    async def async_update(self):
        _LOGGER = logging.getLogger(__name__)
        #_LOGGER.debug("This is a debug message")
        feed = await self.hass.async_add_executor_job(feedparser.parse, self._url)
        #_LOGGER.debug(feed.entries)
        if feed and feed.entries:
            self._state = "Loaded"
            self._attr_extra_state_attributes = {
                "entries": [
                    {
                        "title": entry.title,
                        "link": entry.link,
                        "published": entry.published,
                        "media_thumbnail": entry.media_thumbnail,
                        "tags":entry.tags
                    }
                    for entry in feed.entries[:25]  # Get top 10 entries
                ]
            }
        else:
            self._state = "No entries"
            self._attr_extra_state_attributes = {"entries": []}