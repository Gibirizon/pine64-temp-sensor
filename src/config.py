from dataclasses import dataclass
from enum import Enum
from typing import final

LOWER_TEMP_THRESHOLD = 20
MAIL_SECTION = "MAIL"
REQUIRED_MAIL_INFO = ("sender", "password", "server", "port", "recipient")


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


class Colors(Enum):
    RED = "r"
    GREEN = "g"
    BLUE = "b"


@final
class Font:
    TITLE = 16
    LABEL = 12
    WEIGHT = "bold"


@dataclass(frozen=True)
class ChartConfig:
    color: Colors
    title: str
    xlabel: str
    ylabel: str
    label: str
    filename: str
    facecolor: str = "#f8f9fa"
    alpha: float = 0.3
    legend: str = "upper left"
    marker: str = "o"
    linewidth: int = 2
    markersize: int = 4
    dpi: int = 300
    figsize: tuple[int, int] = (12, 6)


@final
class Chart:
    TEMPERATURE = ChartConfig(
        color=Colors.BLUE,
        title="Temperature Over Time",
        xlabel="Time",
        ylabel="Temperature (°C)",
        label="Temperature",
        filename="temperature.png",
    )
    HUMIDITY = ChartConfig(
        color=Colors.GREEN,
        title="Humidity Over Time",
        xlabel="Time",
        ylabel="Relative Humidity (%)",
        label="Humidity",
        filename="humidity.png",
    )
