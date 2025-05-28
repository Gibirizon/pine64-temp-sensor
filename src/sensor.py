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

    def get_temperature(self, config: SensorConfig) -> float:
        """
        Read temperature from the sensor.

        Returns:
            Temperature in Celsius
        """
        with SMBus(self.i2c_bus) as bus:
            # Write the TEMP_NO_HOLD command
            bus.write_byte(self.device_address, config.measure)

            # Wait for the measurement to complete
            time.sleep(self.measurement_delay)

            # Read 2 bytes of data
            msb = bus.read_byte(self.device_address)
            lsb = bus.read_byte(self.device_address)

            # Calculate temperature
            data = ((msb << 8) | lsb) & 0xFFFC
            temp_c = config.offset + (config.multiplier * float(data) / 65536.0)

            return temp_c

    def get_humidity(self, config: SensorConfig) -> float:
        """
        Read relative humidity from the sensor.

        Returns:
            Relative humidity as percentage
        """
        with SMBus(self.i2c_bus) as bus:
            # Write the HUMIDITY command
            bus.write_byte(self.device_address, config.measure)

            # Wait for the measurement to complete
            time.sleep(self.measurement_delay)

            # Read 2 bytes of data
            msb = bus.read_byte(self.device_address)
            lsb = bus.read_byte(self.device_address)

            # Calculate humidity
            data = ((msb << 8) | lsb) & 0xFFFC
            humidity = ((config.multiplier * data) // 65536) - config.offset

            return humidity
