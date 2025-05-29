# pyright: reportUnknownMemberType=false,  reportUnusedCallResult=false

from datetime import datetime
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from .database import Measurement


class ChartGenerator:
    """Generates and saves charts for sensor measurement data."""

    _output_dir: Path

    def __init__(self, output_dir: str = "charts"):
        """
        Initialize the chart generator.

        Args:
            output_dir: Directory to save chart files
        """
        self._output_dir = Path(output_dir)
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist."""
        self._output_dir.mkdir(parents=True, exist_ok=True)

    def generate_charts(self, measurements: list[Measurement]):
        """
        Generate and save temperature and humidity charts.

        Args:
            measurements: List of Measurement objects to plot
        """
        if not measurements:
            print("No measurements to plot")
            return

        # Extract data
        timestamps = [m.timestamp for m in measurements]
        temperatures = [m.temperature for m in measurements]
        humidities = [m.humidity for m in measurements]

        # Generate temperature chart
        self._generate_temperature_chart(timestamps, temperatures)

        # Generate humidity chart
        self._generate_humidity_chart(timestamps, humidities)

        # Generate combined chart
        # self._generate_combined_chart(timestamps, temperatures, humidities)

        print(f"Charts saved to {self._output_dir}/")

    def _generate_temperature_chart(
        self, timestamps: list[datetime], temperatures: list[float]
    ):
        """Generate and save temperature chart using OOP matplotlib style."""
        fig, ax = plt.subplots(figsize=(12, 6))

        # Plot temperature data
        ax.plot(
            timestamps,  # pyright: ignore[reportArgumentType]
            temperatures,
            "b-",
            linewidth=2,
            marker="o",
            markersize=4,
            label="Temperature",
        )

        # Configure axes
        ax.set_title("Temperature Over Time", fontsize=16, fontweight="bold")
        ax.set_xlabel("Time", fontsize=12)
        ax.set_ylabel("Temperature (°C)", fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.set_facecolor("#f8f9fa")

        # Format x-axis
        self._format_time_axis(ax, timestamps)

        # Add legend
        ax.legend(loc="upper right")

        fig.tight_layout()

        # Save using pathlib
        output_path = self._output_dir / "temperature.png"
        fig.savefig(output_path, dpi=300, bbox_inches="tight")
        fig.clear()
        plt.close(fig)

    def _generate_humidity_chart(
        self, timestamps: list[datetime], humidities: list[float]
    ):
        """Generate and save humidity chart using OOP matplotlib style."""
        fig = Figure(figsize=(12, 6))
        ax = fig.add_subplot(111)

        # Plot humidity data
        ax.plot(
            timestamps,  # pyright: ignore[reportArgumentType]
            humidities,
            "g-",
            linewidth=2,
            marker="s",
            markersize=4,
            label="Humidity",
        )

        # Configure axes
        ax.set_title("Humidity Over Time", fontsize=16, fontweight="bold")
        ax.set_xlabel("Time", fontsize=12)
        ax.set_ylabel("Relative Humidity (%)", fontsize=12)
        ax.set_ylim(0, 100)  # Humidity is always 0-100%
        ax.grid(True, alpha=0.3)
        ax.set_facecolor("#f8f9fa")

        # Format x-axis
        self._format_time_axis(ax, timestamps)

        # Add legend
        ax.legend(loc="upper right")

        fig.tight_layout()

        # Save using pathlib
        output_path = self._output_dir / "humidity.png"
        fig.savefig(output_path, dpi=300, bbox_inches="tight")
        fig.clear()
        plt.close(fig)

    def _format_time_axis(self, ax: Axes, timestamps: list[datetime]):
        """Format the time axis for better readability."""
        if len(timestamps) > 1:
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
            interval = max(1, len(timestamps) // 10)
            # ax.xaxis.set_major_locator(mdates.HourLocator(interval=interval))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())

            # Rotate labels for better readability
            for label in ax.get_xticklabels():
                label.set_rotation(45)
                label.set_horizontalalignment("right")
