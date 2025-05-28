from dataclasses import dataclass
from typing import final


@dataclass(frozen=True)
class SensorConfig:
    measure: int
    offset: float
    multiplier: float


@final
class Sensor:
    TEMPERATURE = SensorConfig(measure=0xF3, offset=-46.85, multiplier=175.72)
    HUMIDITY = SensorConfig(measure=0xF5, offset=-6, multiplier=125)
