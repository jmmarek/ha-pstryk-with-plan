import logging
from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorDeviceClass,
    SensorEntityDescription,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import UnitOfTime
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from homeassistant.helpers.device_registry import DeviceInfo


_LOGGER = logging.getLogger(__name__)


@dataclass
class DescriptionWithWindowSize(SensorEntityDescription):
    window_id: int = 0


@dataclass
class DescriptionWithHour(SensorEntityDescription):
    hour_id: int = 0
    window_id: int = 0


TIME_SENSORS = [
    DescriptionWithWindowSize(
        key="cheapest_hour",
        window_id=0,
        name="Cheapest hour",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    DescriptionWithWindowSize(
        window_id=1,
        key="cheapest_2_hours",
        name="Cheapest 2 hours",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
    DescriptionWithWindowSize(
        window_id=2,
        key="cheapest_3_hours",
        name="Cheapest 3 hours",
        device_class=SensorDeviceClass.TIMESTAMP,
    ),
]

PRICE_SENSORS = [
    DescriptionWithWindowSize(
        window_id=0,
        key="cheapest_hour_price",
        name="Cheapest price",
        native_unit_of_measurement="PLN/kWh",
    ),
    DescriptionWithWindowSize(
        window_id=1,
        key="cheapest_2_hours_price",
        name="Cheapest 2 hours price",
        native_unit_of_measurement="PLN/kWh",
    ),
    DescriptionWithWindowSize(
        window_id=2,
        key="cheapest_3_hours_price",
        name="Cheapest 3 hours price",
        native_unit_of_measurement="PLN/kWh",
    ),
]

CURRENT_PRICE_SENSORS = [
    DescriptionWithHour(
        window_id=0,
        hour_id=0,
        key="current_hour_price",
        name="Current hour price",
        native_unit_of_measurement="PLN/kWh",
    ),
    DescriptionWithHour(
        window_id=1,
        hour_id=1,
        key="current_hour_2_hours_mean_price",
        name="Current hour 2 hours mean price",
        native_unit_of_measurement="PLN/kWh",
    ),
    DescriptionWithHour(
        window_id=0,
        hour_id=1,
        key="next_hour_price",
        name="Next hour price",
        native_unit_of_measurement="PLN/kWh",
    ),
]

CURRENT_WINDOWS = [
    DescriptionWithWindowSize(
        window_id=0,
        key="is_cheapest_hour",
        name="Is cheapest hour now",
    ),
    DescriptionWithWindowSize(
        window_id=1,
        key="is_in_cheapest_2_hours_window",
        name="Is in cheapest 2 hours now",
    ),
    DescriptionWithWindowSize(
        window_id=2,
        key="is_in_cheapest_3_hours_window",
        name="Is in cheapest 3 hours now",
    ),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = entry.runtime_data

    async_add_entities(
        CheapestWindowHourSensor(coordinator, description)
        for description in TIME_SENSORS
    )

    async_add_entities(
        CheapestWindowPriceSensor(coordinator, description)
        for description in PRICE_SENSORS
    )

    async_add_entities(
        IsInCheapestWindowHourSensor(coordinator, description)
        for description in CURRENT_WINDOWS
    )

    async_add_entities(
        CurrentHourPriceSensor(coordinator, description)
        for description in CURRENT_PRICE_SENSORS
    )


class PstrykWithPlanSensorEntity(CoordinatorEntity, SensorEntity):
    def __init__(
        self, coordinator, description: SensorEntityDescription, now=datetime.now
    ):
        super().__init__(coordinator)
        self._attr_unique_id = f"pstryk_with_plan_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={("pstryk_with_plan", "pstryk")},
            name="Pstryk",
            manufacturer="Pstryk",
        )
        self.entity_description = description
        self.now = now


class CheapestWindowHourSensor(PstrykWithPlanSensorEntity):
    @property
    def native_value(self):
        begin_hour = self.coordinator.data["begin_hour"]
        time_difference = self.now(timezone.utc) - begin_hour
        now_hour_from_begining = int((time_difference.total_seconds() / 3600))

        data_hour_prices = self.coordinator.data["window_prices"][
            self.entity_description.window_id
        ]

        data_hour_prices_futures = data_hour_prices[now_hour_from_begining:]
        min_value = min(data_hour_prices_futures)
        hour = data_hour_prices_futures.index(min_value) + now_hour_from_begining
        return begin_hour + timedelta(hours=hour)


class IsInCheapestWindowHourSensor(PstrykWithPlanSensorEntity):
    @property
    def native_value(self):
        begin_hour = self.coordinator.data["begin_hour"]
        time_difference = self.now(timezone.utc) - begin_hour

        current_hour = int((time_difference.total_seconds() / 3600))

        data_hour_prices = self.coordinator.data["window_prices"][
            self.entity_description.window_id
        ]

        min_value = min(data_hour_prices)
        hour = data_hour_prices.index(min_value)
        return hour <= current_hour < hour + 1 + self.entity_description.window_id


class CheapestWindowPriceSensor(PstrykWithPlanSensorEntity):
    @property
    def native_value(self):
        begin_hour = self.coordinator.data["begin_hour"]
        time_difference = self.now(timezone.utc) - begin_hour
        now_hour_from_begining = int((time_difference.total_seconds() / 3600))

        data_hour_prices = self.coordinator.data["window_prices"][
            self.entity_description.window_id
        ]

        return min(data_hour_prices[now_hour_from_begining:])


class CurrentHourPriceSensor(PstrykWithPlanSensorEntity):
    @property
    def native_value(self):
        begin_hour = self.coordinator.data["begin_hour"]
        data_hour_prices = self.coordinator.data["window_prices"][
            self.entity_description.window_id
        ]
        time_difference = self.now(timezone.utc) - begin_hour
        current_hour = (
            int((time_difference.total_seconds() / 3600))
            + self.entity_description.hour_id
        )
        return data_hour_prices[current_hour]
