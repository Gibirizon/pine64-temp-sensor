import time

from smbus2 import SMBus

from src.config import SensorConfig


class TemperatureHumiditySensor:
    """Interface for I2C temperature and humidity sensor."""

    i2c_bus: int
    device_address: int
    measurement_delay: float

    def __init__(self, i2c_bus: int = 0, device_address: int = 0x40):
        """
        Initialize the sensor.

        Args:
            i2c_bus: I2C bus number
            device_address: I2C device address
        """
        self.i2c_bus = i2c_bus
        self.device_address = device_address
        self.measurement_delay = 0.5  # seconds

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
