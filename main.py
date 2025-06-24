"""
Main entry point for the temperature and humidity monitoring system.
"""

import argparse
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


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        "-s",
        "--setup_file",
        metavar="setupfile",
        help="setup file containing parameters for mail sending",
        required=True,
        type=str,
    )

    args = parser.parse_args()
    return args


def main():
    configure_logging()

    mail_args = parse_arguments()
    system = MeasurementSystem(setup_file=mail_args.setup_file)  # pyright: ignore[reportAny]
    system.run_measurement()


if __name__ == "__main__":
    main()
