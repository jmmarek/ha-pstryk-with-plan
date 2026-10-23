import aiohttp
import logging
from datetime import timedelta
from homeassistant.exceptions import ConfigEntryAuthFailed, HomeAssistantError
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)


class PstrykApi:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def async_get_data(self):
        headers = {
            "Authorization": f"{self.api_key}",
        }

        warsaw_now = dt_util.now()
        warsaw_midnight = dt_util.start_of_local_day(warsaw_now)

        utc_midnight = warsaw_midnight.astimezone(dt_util.UTC)
        start_formatted = utc_midnight.isoformat().replace("+00:00", "Z")

        warsaw_end = warsaw_midnight + timedelta(days=2) - timedelta(microseconds=1)
        utc_end = warsaw_end.astimezone(dt_util.UTC)
        end_formatted = utc_end.isoformat().replace("+00:00", "Z")
        _LOGGER.debug("Fetch start: %s, end: %s", start_formatted, end_formatted)
        async with (
            aiohttp.ClientSession() as session,
            session.get(
                f"https://api.pstryk.pl/integrations/meter-data/unified-metrics/?metrics=pricing&window_start={start_formatted}&window_end={end_formatted}&resolution=hour",
                headers=headers,
            ) as response,
        ):
            if response.status == 401:
                raise ConfigEntryAuthFailed

            if response.status != 200:
                raise HomeAssistantError(f"API returned HTTP status {response.status}")

            return await response.json(), warsaw_midnight

    async def async_validate(self) -> dict:
        return self.async_get_data()
