from homeassistant.core import callback
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
)
from homeassistant.helpers.event import async_track_time_change
import logging
import asyncio

from .api import PstrykApi

_LOGGER = logging.getLogger(__name__)


def get_sum_of_n(n, hour_prices_slice):
    sum = 0
    for i in range(n):
        sum += hour_prices_slice[i]
    return sum


def get_n_hour_window(window_len, hour_prices):
    return [
        get_sum_of_n(window_len, hour_prices[i:]) / window_len
        for i in range(len(hour_prices) - window_len + 1)
    ]


class PstrykCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, api: PstrykApi):
        self.api = api

        super().__init__(
            hass,
            _LOGGER,
            name="PstrykWithPlan integration",
            update_interval=None,
        )

        self._remove_api_timer = async_track_time_change(
            hass,
            self._api_update,
            hour=[13],
            minute=0,
            second=0,
        )

        self._remove_hour_listener = async_track_time_change(
            hass,
            self._hour_changed,
            minute=0,
            second=0,
        )

    async def _async_update_data(self):
        _LOGGER.warning("Try updating data")
        try:
            async with asyncio.timeout(120):
                _LOGGER.debug("waited... now return")
                raw_data, start_time = await self.api.async_get_data()
                hour_prices = [
                    frame["metrics"]["pricing"]["full_price"]
                    for frame in raw_data["frames"]
                    if frame["metrics"]["pricing"]["full_price"] is not None
                ]
                average_prices_windows = [hour_prices]
                for window_len in range(2, 4):
                    average_prices_windows.append(
                        get_n_hour_window(window_len, hour_prices)
                    )

                result = {
                    "begin_hour": start_time,
                    "window_prices": average_prices_windows,
                }

                return result
        except ConfigEntryAuthFailed as err:
            raise

    @callback
    def _hour_changed(self, now):
        self.async_update_listeners()

    @callback
    def _api_update(self, now):
        self.hass.async_create_task(self.async_request_refresh())

    async def async_shutdown(self):
        self._remove_hour_listener()
        await super().async_shutdown()
