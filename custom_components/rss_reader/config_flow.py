from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN

class RSSReaderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Split the comma-separated string into a list
            feeds_raw = user_input.get("feeds", "")
            feeds = [url.strip() for url in feeds_raw.split(",") if url.strip()]
            return self.async_create_entry(title="RSS Feeds", data={"feeds": feeds})

        schema = vol.Schema({
            vol.Required("feeds"): str  # Ask user to enter comma-separated feed URLs
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
