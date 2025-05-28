import logging
import time
from datetime import datetime

from smbus2 import SMBus

from src.config import Sensor, SensorConfig

logger = logging.getLogger(__name__)


class MeasurementSystem:
    """Orchestrates the complete measurement workflow."""

    i2c_bus: int
    device_address: int
    measurement_delay: float

    def __init__(
        self,
        i2c_bus: int = 0,
        device_address: int = 0x40,
        measurement_delay: float = 0.5,
    ):
        """
        Initialize the measurement system.

        Args:
            i2c_bus: I2C bus number
            device_address: I2C device address
        """
        self.i2c_bus = i2c_bus
        self.device_address = device_address
        self.measurement_delay = measurement_delay  # seconds

    def run_measurement(self):
        """
        Run a single measurement cycle: read sensor, store data, generate charts.

        Returns:
            Tuple of (temperature, humidity, timestamp) if successful, None otherwise
        """
        try:
            # Read sensor data
            logger.info("Reading sensor data...")
            temperature = self.get_temperature_or_humidity(Sensor.TEMPERATURE)
            humidity = self.get_temperature_or_humidity(Sensor.HUMIDITY)
            timestamp = datetime.now()

            logger.info(f"Measured: temp={temperature:.2f}°C, humidity={humidity:.2f}%")

        except Exception as e:
            logger.error(f"Error during measurement cycle: {e}")

    def get_temperature_or_humidity(self, measurement_type: SensorConfig) -> float:
        """
        Read temperature/humidity from the sensor.

        Returns:
            Measured data
        """
        with SMBus(self.i2c_bus) as bus:
            # Write the TEMP_NO_HOLD or HUMIDITY_NO_HOLD command
            bus.write_byte(self.device_address, measurement_type.measure)

            # Wait for the measurement to complete
            time.sleep(self.measurement_delay)

            # Read 2 bytes of data
            most_significant_byte = bus.read_byte(self.device_address)
            least_significant_byte = bus.read_byte(self.device_address)

            # Calculate temperature / humidity based on constants values
            data = ((most_significant_byte << 8) | least_significant_byte) & 0xFFFC
            converted_result = measurement_type.offset + (
                measurement_type.multiplier * float(data) / 65536.0
            )

            return converted_result
