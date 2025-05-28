"""
Main entry point for the temperature and humidity monitoring system.
"""

import logging

from src.measurement_system import MeasurementSystem


def configure_logging():
    file_handler = logging.FileHandler("measurement.log")
    stream_handler = logging.StreamHandler()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[file_handler, stream_handler],
    )


def main():
    configure_logging()

    system = MeasurementSystem()
    system.run_measurement()


if __name__ == "__main__":
    main()
