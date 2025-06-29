import logging
import time
from datetime import datetime
from pathlib import Path

from smbus2 import SMBus

from src.chart_generator import ChartGenerator
from src.config import LOWER_TEMP_THRESHOLD, Sensor, SensorConfig
from src.database import DatabaseManager
from src.mailer import Mailer

logger = logging.getLogger(__name__)


class MeasurementSystem:
    """Orchestrates the complete measurement workflow."""

    _i2c_bus: int
    _device_address: int
    _measurement_delay: float
    _chart_generator: ChartGenerator
    _setup_file: Path

    def __init__(
        self,
        i2c_bus: int = 0,
        device_address: int = 0x40,
        measurement_delay: float = 0.5,
        setup_file: str = "config.ini",
    ):
        """
        Initialize the measurement system.

        Args:
            i2c_bus: I2C bus number
            device_address: I2C device address
        """
        self._i2c_bus = i2c_bus
        self._device_address = device_address
        self._measurement_delay = measurement_delay  # seconds
        self._setup_file = Path(setup_file)

        self._chart_generator = ChartGenerator()

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
            logger.info(f"Measured: temp={temperature:.2f}°C, humidity={humidity:.2f}%")

            timestamp = datetime.now()

            # Store in database
            logger.info("Storing data in database...")
            with DatabaseManager() as db_manager:
                db_manager.insert_measurement(temperature, humidity, timestamp)
                all_measurements = db_manager.get_all_measurements()
                logger.info(all_measurements)

            # Generate charts
            logger.info("Generating charts...")
            self._chart_generator.generate_charts(all_measurements)

            logger.info("Measurement cycle completed successfully")

        except Exception as e:
            logger.error(f"Error during measurement cycle: {e}")

    def get_temperature_or_humidity(self, measurement_type: SensorConfig) -> float:
        """
        Read temperature/humidity from the sensor.

        Returns:
            Measured data
        """
        with SMBus(self._i2c_bus) as bus:
            # Write the TEMP_NO_HOLD or HUMIDITY_NO_HOLD command
            bus.write_byte(self._device_address, measurement_type.measure)

            # Wait for the measurement to complete
            time.sleep(self._measurement_delay)

            # Read 2 bytes of data
            most_significant_byte = bus.read_byte(self._device_address)
            least_significant_byte = bus.read_byte(self._device_address)

            # Calculate temperature / humidity based on constants values
            data = ((most_significant_byte << 8) | least_significant_byte) & 0xFFFC
            converted_result = measurement_type.offset + (
                measurement_type.multiplier * float(data) / 65536.0
            )

            if (
                measurement_type == Sensor.TEMPERATURE
                and LOWER_TEMP_THRESHOLD >= converted_result
            ):
                self.notify_low_temperature(converted_result)

            return converted_result

    def notify_low_temperature(self, temperature: float):
        logger.warning(f"Temperature is below threshold: {temperature:.2f}°C")
        mailer = Mailer(self._setup_file)
        mailer.send_email(temperature)
