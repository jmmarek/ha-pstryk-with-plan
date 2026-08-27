"""Sensor test cases for the Pstryk with plan"""

from collections.abc import Generator
from unittest.mock import AsyncMock, Mock, patch, MagicMock
from custom_components.pstryk_with_plan.sensor import (
    CheapestWindowHourSensor,
    CheapestWindowPriceSensor,
    CurrentHourPriceSensor,
    IsInCheapestWindowHourSensor,
)
from datetime import datetime, timezone


async def test_sensor_cheapest_hour(hass):
    coordinator = Mock()

    entity_description = Mock()
    entity_description.window_id = 0

    coordinator.data = {
        "begin_hour": datetime(2026, 7, 24, 1, 0, tzinfo=timezone.utc),
        "window_prices": [[7, 6, 3, 4, 5, 6, 7, 4, 9]],
    }

    magic_now = MagicMock(return_value=datetime(2026, 7, 24, 1, 0, tzinfo=timezone.utc))
    sensor = CheapestWindowHourSensor(coordinator, entity_description, now=magic_now)

    assert sensor.native_value == datetime(2026, 7, 24, 1 + 2, 0, tzinfo=timezone.utc)


async def test_sensor_cheapest_hour_after_time(hass):
    coordinator = Mock()

    entity_description = Mock()
    entity_description.window_id = 0

    coordinator.data = {
        "begin_hour": datetime(2026, 7, 24, 1, 0, tzinfo=timezone.utc),
        "window_prices": [[7, 6, 3, 4, 5, 6, 7, 4, 9]],
    }

    magic_now = MagicMock(
        return_value=datetime(2026, 7, 24, 5, 12, tzinfo=timezone.utc)
    )
    sensor = CheapestWindowHourSensor(coordinator, entity_description, now=magic_now)

    assert sensor.native_value == datetime(2026, 7, 24, 1 + 7, 0, tzinfo=timezone.utc)


async def test_sensor_cheapest_price(hass):
    coordinator = Mock()

    entity_description = Mock()
    entity_description.window_id = 0

    coordinator.data = {
        "begin_hour": datetime(2026, 7, 24, 1, 0, tzinfo=timezone.utc),
        "window_prices": [[7, 6, 3, 4, 5, 6, 7, 4, 9]],
    }

    magic_now = MagicMock(
        return_value=datetime(2026, 7, 24, 1, 12, tzinfo=timezone.utc)
    )
    sensor = CheapestWindowPriceSensor(coordinator, entity_description, now=magic_now)

    assert sensor.native_value == 3


async def test_sensor_cheapest_price_after_time(hass):
    coordinator = Mock()

    entity_description = Mock()
    entity_description.window_id = 0

    coordinator.data = {
        "begin_hour": datetime(2026, 7, 24, 1, 0, tzinfo=timezone.utc),
        "window_prices": [[7, 6, 3, 4, 5, 6, 7, 4, 9]],
    }

    magic_now = MagicMock(
        return_value=datetime(2026, 7, 24, 5, 12, tzinfo=timezone.utc)
    )
    sensor = CheapestWindowPriceSensor(coordinator, entity_description, now=magic_now)

    assert sensor.native_value == 4


async def test_sensor_current_hour_price(hass):
    coordinator = Mock()

    entity_description = Mock()
    entity_description.window_id = 0
    entity_description.hour_id = 0

    coordinator.data = {
        "begin_hour": datetime(2026, 8, 19, 1, 0, tzinfo=timezone.utc),
        "window_prices": [[0, 1, 2, 3, 4, 5, 1.3, 9]],
    }

    magic_now = MagicMock(
        return_value=datetime(2026, 8, 19, 7, 12, tzinfo=timezone.utc)
    )
    sensor = CurrentHourPriceSensor(coordinator, entity_description, magic_now)

    # 7th Hour is 6th from begin_hour
    assert sensor.native_value == 1.3


async def test_sensor_next_hour_price(hass):
    coordinator = Mock()

    entity_description = Mock()
    entity_description.window_id = 0
    entity_description.hour_id = 1

    coordinator.data = {
        "begin_hour": datetime(2026, 8, 19, 1, 0, tzinfo=timezone.utc),
        "window_prices": [[0, 1, 2, 3, 4, 5, 1.3, 9]],
    }

    magic_now = MagicMock(
        return_value=datetime(2026, 8, 19, 7, 12, tzinfo=timezone.utc)
    )
    sensor = CurrentHourPriceSensor(coordinator, entity_description, magic_now)

    # 7th Hour is 6th from begin_hour + 1
    assert sensor.native_value == 9


async def test_sensor_is_in_cheapest_price(hass):
    coordinator = Mock()

    entity_description = Mock()
    entity_description.window_id = 0

    coordinator.data = {
        "begin_hour": datetime(2026, 8, 28, 1, 0, tzinfo=timezone.utc),
        "window_prices": [[7, 6, 3, 1, 2, 6, 7, 4, 9]],
    }

    magic_now = MagicMock(
        return_value=datetime(2026, 8, 28, 4, 12, tzinfo=timezone.utc)
    )
    sensor = IsInCheapestWindowHourSensor(
        coordinator, entity_description, now=magic_now
    )

    assert sensor.native_value


async def test_sensor_is_in_cheapest_price_2_hours_window(hass):
    coordinator = Mock()

    entity_description = Mock()
    entity_description.window_id = 1

    coordinator.data = {
        "begin_hour": datetime(2026, 8, 28, 1, 0, tzinfo=timezone.utc),
        "window_prices": [[], [7, 6, 3, 1, 6, 6, 7, 4, 9]],
    }

    magic_now = MagicMock(
        return_value=datetime(2026, 8, 28, 4, 12, tzinfo=timezone.utc)
    )
    sensor = IsInCheapestWindowHourSensor(
        coordinator, entity_description, now=magic_now
    )

    assert sensor.native_value

    magic_now = MagicMock(return_value=datetime(2026, 8, 28, 5, 5, tzinfo=timezone.utc))
    sensor = IsInCheapestWindowHourSensor(
        coordinator, entity_description, now=magic_now
    )

    assert sensor.native_value


async def test_sensor_is_not_in_cheapest_price(hass):
    coordinator = Mock()

    entity_description = Mock()
    entity_description.window_id = 0

    coordinator.data = {
        "begin_hour": datetime(2026, 8, 28, 1, 0, tzinfo=timezone.utc),
        "window_prices": [[7, 6, 3, 1, 2, 6, 7, 4, 9]],
    }

    magic_now = MagicMock(return_value=datetime(2026, 8, 28, 3, 0, tzinfo=timezone.utc))
    sensor = IsInCheapestWindowHourSensor(
        coordinator, entity_description, now=magic_now
    )

    assert not sensor.native_value

    magic_now = MagicMock(return_value=datetime(2026, 8, 28, 5, 0, tzinfo=timezone.utc))
    sensor = IsInCheapestWindowHourSensor(
        coordinator, entity_description, now=magic_now
    )

    assert not sensor.native_value


async def test_sensor_is_not_in_cheapest_price_2_hours_window(hass):
    coordinator = Mock()

    entity_description = Mock()
    entity_description.window_id = 1

    coordinator.data = {
        "begin_hour": datetime(2026, 8, 28, 1, 0, tzinfo=timezone.utc),
        "window_prices": [[], [7, 6, 3, 1, 2, 6, 7, 4, 9]],
    }

    magic_now = MagicMock(return_value=datetime(2026, 8, 28, 3, 0, tzinfo=timezone.utc))
    sensor = IsInCheapestWindowHourSensor(
        coordinator, entity_description, now=magic_now
    )

    assert not sensor.native_value

    magic_now = MagicMock(return_value=datetime(2026, 8, 28, 6, 0, tzinfo=timezone.utc))
    sensor = IsInCheapestWindowHourSensor(
        coordinator, entity_description, now=magic_now
    )

    assert not sensor.native_value
