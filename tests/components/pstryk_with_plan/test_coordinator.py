"""Common fixtures for the Pstryk with plan tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, Mock, patch
from custom_components.pstryk_with_plan.coordinator import PstrykCoordinator
from datetime import datetime

import pytest
import json


json_string = """
{
  "frames": [
    {
      "start": "2026-07-24T00:00:00Z",
      "end": "2026-07-24T01:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.63453,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.1049300000000002,
          "vat_component": 0.2541339000000001,
          "excise_component": 0.005,
          "full_price": 1.3640639,
          "price_net": 0.63453,
          "price_gross": 1.3640639,
          "price_prosumer_net": 0.63453,
          "price_prosumer_gross": 0.7804719,
          "is_cheap": false,
          "is_expensive": true
        }
      }
    },
    {
      "start": "2026-07-24T01:00:00Z",
      "end": "2026-07-24T02:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.62577,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.09617,
          "vat_component": 0.25211910000000004,
          "excise_component": 0.005,
          "full_price": 1.3532891,
          "price_net": 0.62577,
          "price_gross": 1.3532891,
          "price_prosumer_net": 0.62577,
          "price_prosumer_gross": 0.7696971,
          "is_cheap": false,
          "is_expensive": true
        }
      }
    },
    {
      "start": "2026-07-24T02:00:00Z",
      "end": "2026-07-24T03:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.63548,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.1058800000000002,
          "vat_component": 0.25435240000000003,
          "excise_component": 0.005,
          "full_price": 1.3652324,
          "price_net": 0.63548,
          "price_gross": 1.3652324,
          "price_prosumer_net": 0.63548,
          "price_prosumer_gross": 0.7816404,
          "is_cheap": false,
          "is_expensive": true
        }
      }
    },
    {
      "start": "2026-07-24T03:00:00Z",
      "end": "2026-07-24T04:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.66301,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.13341,
          "vat_component": 0.26068430000000004,
          "excise_component": 0.005,
          "full_price": 1.3990943,
          "price_net": 0.66301,
          "price_gross": 1.3990943,
          "price_prosumer_net": 0.66301,
          "price_prosumer_gross": 0.8155023,
          "is_cheap": false,
          "is_expensive": true
        }
      }
    },
    {
      "start": "2026-07-24T04:00:00Z",
      "end": "2026-07-24T05:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.71901,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.18941,
          "vat_component": 0.27356430000000004,
          "excise_component": 0.005,
          "full_price": 1.4679743,
          "price_net": 0.71901,
          "price_gross": 1.4679743,
          "price_prosumer_net": 0.71901,
          "price_prosumer_gross": 0.8843823000000001,
          "is_cheap": false,
          "is_expensive": true
        }
      }
    },
    {
      "start": "2026-07-24T05:00:00Z",
      "end": "2026-07-24T06:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.7165900000000001,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.1869900000000002,
          "vat_component": 0.2730077000000001,
          "excise_component": 0.005,
          "full_price": 1.4649977,
          "price_net": 0.7165900000000001,
          "price_gross": 1.4649977,
          "price_prosumer_net": 0.7165900000000001,
          "price_prosumer_gross": 0.8814057000000001,
          "is_cheap": false,
          "is_expensive": true
        }
      },
      "is_live": true
    },
    {
      "start": "2026-07-24T06:00:00Z",
      "end": "2026-07-24T07:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.63336,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.10376,
          "vat_component": 0.2538648,
          "excise_component": 0.005,
          "full_price": 1.3626247999999999,
          "price_net": 0.63336,
          "price_gross": 1.3626247999999999,
          "price_prosumer_net": 0.63336,
          "price_prosumer_gross": 0.7790328000000001,
          "is_cheap": false,
          "is_expensive": true
        }
      }
    },
    {
      "start": "2026-07-24T07:00:00Z",
      "end": "2026-07-24T08:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.53101,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.0014100000000001,
          "vat_component": 0.23032430000000004,
          "excise_component": 0.005,
          "full_price": 1.2367343,
          "price_net": 0.53101,
          "price_gross": 1.2367343,
          "price_prosumer_net": 0.53101,
          "price_prosumer_gross": 0.6531423,
          "is_cheap": false,
          "is_expensive": false
        }
      }
    },
    {
      "start": "2026-07-24T08:00:00Z",
      "end": "2026-07-24T09:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.44403,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 0.91443,
          "vat_component": 0.2103189,
          "excise_component": 0.005,
          "full_price": 1.1297488999999998,
          "price_net": 0.44403,
          "price_gross": 1.1297488999999998,
          "price_prosumer_net": 0.44403,
          "price_prosumer_gross": 0.5461569,
          "is_cheap": false,
          "is_expensive": false
        }
      }
    },
    {
      "start": "2026-07-24T09:00:00Z",
      "end": "2026-07-24T10:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.38187,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 0.85227,
          "vat_component": 0.1960221,
          "excise_component": 0.005,
          "full_price": 1.0532921,
          "price_net": 0.38187,
          "price_gross": 1.0532921,
          "price_prosumer_net": 0.38187,
          "price_prosumer_gross": 0.46970009999999995,
          "is_cheap": false,
          "is_expensive": false
        }
      }
    },
    {
      "start": "2026-07-24T10:00:00Z",
      "end": "2026-07-24T11:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.28516,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 0.75556,
          "vat_component": 0.1737788,
          "excise_component": 0.005,
          "full_price": 0.9343388,
          "price_net": 0.28516,
          "price_gross": 0.9343388,
          "price_prosumer_net": 0.28516,
          "price_prosumer_gross": 0.3507468,
          "is_cheap": false,
          "is_expensive": false
        }
      }
    },
    {
      "start": "2026-07-24T11:00:00Z",
      "end": "2026-07-24T12:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.22369,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 0.69409,
          "vat_component": 0.1596407,
          "excise_component": 0.005,
          "full_price": 0.8587307,
          "price_net": 0.22369,
          "price_gross": 0.8587307,
          "price_prosumer_net": 0.22369,
          "price_prosumer_gross": 0.2751387,
          "is_cheap": false,
          "is_expensive": false
        }
      }
    },
    {
      "start": "2026-07-24T12:00:00Z",
      "end": "2026-07-24T13:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.19307,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 0.66347,
          "vat_component": 0.15259810000000001,
          "excise_component": 0.005,
          "full_price": 0.8210681,
          "price_net": 0.19307,
          "price_gross": 0.8210681,
          "price_prosumer_net": 0.19307,
          "price_prosumer_gross": 0.2374761,
          "is_cheap": false,
          "is_expensive": false
        }
      }
    },
    {
      "start": "2026-07-24T13:00:00Z",
      "end": "2026-07-24T14:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.30499000000000004,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 0.77539,
          "vat_component": 0.17833970000000002,
          "excise_component": 0.005,
          "full_price": 0.9587297,
          "price_net": 0.30499000000000004,
          "price_gross": 0.9587297,
          "price_prosumer_net": 0.30499000000000004,
          "price_prosumer_gross": 0.3751377,
          "is_cheap": false,
          "is_expensive": false
        }
      }
    },
    {
      "start": "2026-07-24T14:00:00Z",
      "end": "2026-07-24T15:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.42701,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 0.8974099999999999,
          "vat_component": 0.20640429999999999,
          "excise_component": 0.005,
          "full_price": 1.1088142999999997,
          "price_net": 0.42701,
          "price_gross": 1.1088142999999997,
          "price_prosumer_net": 0.42701,
          "price_prosumer_gross": 0.5252223,
          "is_cheap": false,
          "is_expensive": false
        }
      }
    },
    {
      "start": "2026-07-24T15:00:00Z",
      "end": "2026-07-24T16:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.49624,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 0.96664,
          "vat_component": 0.22232720000000003,
          "excise_component": 0.005,
          "full_price": 1.1939672,
          "price_net": 0.49624,
          "price_gross": 1.1939672,
          "price_prosumer_net": 0.49624,
          "price_prosumer_gross": 0.6103752,
          "is_cheap": false,
          "is_expensive": false
        }
      }
    },
    {
      "start": "2026-07-24T16:00:00Z",
      "end": "2026-07-24T17:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.64818,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.1185800000000001,
          "vat_component": 0.25727340000000004,
          "excise_component": 0.005,
          "full_price": 1.3808534000000001,
          "price_net": 0.64818,
          "price_gross": 1.3808534000000001,
          "price_prosumer_net": 0.64818,
          "price_prosumer_gross": 0.7972614,
          "is_cheap": false,
          "is_expensive": true
        }
      }
    },
    {
      "start": "2026-07-24T17:00:00Z",
      "end": "2026-07-24T18:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.81087,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.2812700000000001,
          "vat_component": 0.29469210000000007,
          "excise_component": 0.005,
          "full_price": 1.5809621,
          "price_net": 0.81087,
          "price_gross": 1.5809621,
          "price_prosumer_net": 0.81087,
          "price_prosumer_gross": 0.9973700999999999,
          "is_cheap": false,
          "is_expensive": true
        }
      }
    },
    {
      "start": "2026-07-24T18:00:00Z",
      "end": "2026-07-24T19:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.94908,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.41948,
          "vat_component": 0.3264804,
          "excise_component": 0.005,
          "full_price": 1.7509603999999999,
          "price_net": 0.94908,
          "price_gross": 1.7509603999999999,
          "price_prosumer_net": 0.94908,
          "price_prosumer_gross": 1.1673684,
          "is_cheap": false,
          "is_expensive": true
        }
      }
    },
    {
      "start": "2026-07-24T19:00:00Z",
      "end": "2026-07-24T20:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.94899,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.4193900000000002,
          "vat_component": 0.3264597000000001,
          "excise_component": 0.005,
          "full_price": 1.7508497,
          "price_net": 0.94899,
          "price_gross": 1.7508497,
          "price_prosumer_net": 0.94899,
          "price_prosumer_gross": 1.1672577,
          "is_cheap": false,
          "is_expensive": true
        }
      }
    },
    {
      "start": "2026-07-24T20:00:00Z",
      "end": "2026-07-24T21:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.8398300000000001,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.3102300000000002,
          "vat_component": 0.3013529000000001,
          "excise_component": 0.005,
          "full_price": 1.6165829,
          "price_net": 0.8398300000000001,
          "price_gross": 1.6165829,
          "price_prosumer_net": 0.8398300000000001,
          "price_prosumer_gross": 1.0329909000000002,
          "is_cheap": false,
          "is_expensive": true
        }
      }
    },
    {
      "start": "2026-07-24T21:00:00Z",
      "end": "2026-07-24T22:00:00Z",
      "metrics": {
        "pricing": {
          "tge_price": 0.77243,
          "dist_price": 0.3904,
          "service_price": 0.08,
          "base_price": 1.24283,
          "vat_component": 0.2858509,
          "excise_component": 0.005,
          "full_price": 1.5336809,
          "price_net": 0.77243,
          "price_gross": 1.5336809,
          "price_prosumer_net": 0.77243,
          "price_prosumer_gross": 0.9500888999999999,
          "is_cheap": false,
          "is_expensive": true
        }
      }
    },
    {
      "start": "2026-07-24T22:00:00Z",
      "end": "2026-07-24T23:00:00Z",
      "metrics": {
        "pricing": {
          "full_price": 1.433
        }
      }
    },
    {
      "start": "2026-07-24T23:00:00Z",
      "end": "2026-07-25T00:00:00Z",
      "metrics": {
        "pricing": {
          "full_price": 1.401
        }
      }
    }
  ]
}
"""


async def test_coordinator_get_price_per_hour(hass):
    api = Mock()

    api.async_get_data = AsyncMock(
        return_value=(json.loads(json_string), datetime.now())
    )

    coordinator = PstrykCoordinator(hass, api)

    await coordinator.async_refresh()
    assert len(coordinator.data["window_prices"][0]) == 24
    assert coordinator.data["window_prices"][0] == [
        1.3640639,
        1.3532891,
        1.3652324,
        1.3990943,
        1.4679743,
        1.4649977,
        1.3626247999999999,
        1.2367343,
        1.1297488999999998,
        1.0532921,
        0.9343388,
        0.8587307,
        0.8210681,
        0.9587297,
        1.1088142999999997,
        1.1939672,
        1.3808534000000001,
        1.5809621,
        1.7509603999999999,
        1.7508497,
        1.6165829,
        1.5336809,
        1.433,
        1.401,
    ]


async def test_coordinator_get_price_per_3_hour_windows(hass):
    api = Mock()

    api.async_get_data = AsyncMock(
        return_value=(json.loads(json_string), datetime.now())
    )

    coordinator = PstrykCoordinator(hass, api)

    await coordinator.async_refresh()
    assert len(coordinator.data["window_prices"][2]) == 24 - 2
    assert coordinator.data["window_prices"][2] == [
        1.3608618000000001,
        1.3725386000000002,
        1.4107669999999999,
        1.4440221,
        1.4318656,
        1.3547855999999998,
        1.243036,
        1.1399251,
        1.0391266,
        0.9487871999999999,
        0.8713792000000001,
        0.8795095,
        0.9628706999999999,
        1.0871704,
        1.2278782999999998,
        1.3852608999999998,
        1.5709253,
        1.6942574,
        1.706131,
        1.6337045000000001,
        1.5277546,
        1.4558936333333332,
    ]


async def test_coordinator_skip_null_prices(hass):
    json_string = """
    {
      "frames": [
        {
          "start": "2026-07-24T00:00:00Z",
          "end": "2026-07-24T01:00:00Z",
          "metrics": {
            "pricing": {
              "full_price": 1.3640639
            }
          }
        },
        {
          "start": "2026-07-24T01:00:00Z",
          "end": "2026-07-24T02:00:00Z",
          "metrics": {
            "pricing": {
              "full_price": 1.3532891
            }
          }
        },
        {
          "start": "2026-07-24T02:00:00Z",
          "end": "2026-07-24T03:00:00Z",
          "metrics": {
            "pricing": {
              "full_price": null
            }
          }
        }
      ]
    }
    """
    api = Mock()

    api.async_get_data = AsyncMock(
        return_value=(json.loads(json_string), datetime.now())
    )

    coordinator = PstrykCoordinator(hass, api)

    await coordinator.async_refresh()
    assert len(coordinator.data["window_prices"][0]) == 2
    assert coordinator.data["window_prices"][0] == [1.3640639, 1.3532891]
