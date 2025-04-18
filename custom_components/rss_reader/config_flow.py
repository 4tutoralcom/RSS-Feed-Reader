from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN  # or just use a string "rss_reader" if this fails

class RSSReaderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        print('1')
        errors = {}
        if user_input is not None:
            return self.async_create_entry(title="RSS Feeds", data=user_input)

        schema = vol.Schema({
            vol.Required("feeds"): str  # Just let user enter a comma-separated string
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
