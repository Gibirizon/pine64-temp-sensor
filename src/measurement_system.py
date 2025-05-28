import logging
from datetime import datetime

from src.config import Sensor
from src.sensor import TemperatureHumiditySensor

logger = logging.getLogger(__name__)


class MeasurementSystem:
    """Orchestrates the complete measurement workflow."""

    sensor: TemperatureHumiditySensor

    def __init__(self, i2c_bus: int = 0, device_address: int = 0x40):
        """
        Initialize the measurement system.

        Args:
            i2c_bus: I2C bus number
            device_address: I2C device address
        """
        self.sensor = TemperatureHumiditySensor(i2c_bus, device_address)

    def run_measurement(self):
        """
        Run a single measurement cycle: read sensor, store data, generate charts.

        Returns:
            Tuple of (temperature, humidity, timestamp) if successful, None otherwise
        """
        try:
            # Read sensor data
            logger.info("Reading sensor data...")
            temperature = self.sensor.get_temperature(Sensor.TEMPERATURE)
            humidity = self.sensor.get_humidity(Sensor.HUMIDITY)
            timestamp = datetime.now()

            logger.info(f"Measured: temp={temperature:.2f}°C, humidity={humidity}%")

        except Exception as e:
            logger.error(f"Error during measurement cycle: {e}")
