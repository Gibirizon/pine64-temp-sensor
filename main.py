import time

import smbus2

# Constants
TEMP_NO_HOLD = 0xF3
HUMIDITY = 0xF5
DEVICE_ADDRESS = 0x40
I2C_BUS = 0  # /dev/i2c-0


def get_temp(bus):
    # Write the TEMP_NO_HOLD command
    bus.write_byte(DEVICE_ADDRESS, TEMP_NO_HOLD)

    # Wait for the measurement to complete
    time.sleep(0.5)

    # Read 2 bytes of data
    msb = bus.read_byte(DEVICE_ADDRESS)
    lsb = bus.read_byte(DEVICE_ADDRESS)

    # Calculate temperature
    temp = ((msb * 256) + lsb) & 0xFFFC
    temp_c = -46.85 + (175.72 * float(temp) / 65536.0)
    temp_f = temp_c * 1.8 + 32

    return temp_f, temp_c


def get_relative_humidity(bus):
    # Write the HUMIDITY command
    bus.write_byte(DEVICE_ADDRESS, HUMIDITY)

    # Wait for the measurement to complete
    time.sleep(0.5)

    # Read 2 bytes of data
    msb = bus.read_byte(DEVICE_ADDRESS)
    lsb = bus.read_byte(DEVICE_ADDRESS)

    # Calculate humidity
    data = ((msb * 256) + lsb) & 0xFFFC
    humidity = ((125 * data) // 65536) - 6

    return humidity


def main():
    try:
        # Open the I2C bus
        bus = smbus2.SMBus(I2C_BUS)

        # Get temperature and humidity
        temp_f, _ = get_temp(bus)
        humidity = get_relative_humidity(bus)

        print(f"temp={temp_f:.2f} humidity={humidity}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

