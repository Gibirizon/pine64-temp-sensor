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


@final
class Stats:
    UPPER_RIGHT_CORNER = (0.96, 0.96)
    VERTICAL_ALIGNMENT = "top"
    HORIZONTAL_ALIGNMENT = "right"
    ALPHA = 0.8
    PAD = 0.5
    FACECOLOR = "wheat"
