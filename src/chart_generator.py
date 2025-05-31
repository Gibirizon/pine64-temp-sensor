# pyright: reportUnknownMemberType=false,  reportUnusedCallResult=false

from datetime import datetime
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

from src.config import Chart, ChartConfig, Font, Stats
from src.database import Measurement


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
        self._generate_chart(timestamps, temperatures, Chart.TEMPERATURE)

        # Generate humidity chart
        self._generate_chart(timestamps, humidities, Chart.HUMIDITY)

        print(f"Charts saved to {self._output_dir}/")

    def _generate_chart(
        self,
        timestamps: list[datetime],
        measurements: list[float],
        chart_type: ChartConfig,
    ):
        """Generate and save chart using OOP matplotlib style."""
        fig, ax = plt.subplots(figsize=chart_type.figsize)

        # Plot temperature data
        ax.plot(
            timestamps,  # pyright: ignore[reportArgumentType]
            measurements,
            f"{chart_type.color.value}-",
            linewidth=chart_type.linewidth,
            marker=chart_type.marker,
            markersize=chart_type.markersize,
            label=chart_type.label,
        )

        # Configure axes
        ax.set_title(chart_type.title, fontsize=Font.TITLE, fontweight=Font.WEIGHT)
        ax.set_xlabel(chart_type.xlabel, fontsize=Font.LABEL)
        ax.set_ylabel(chart_type.ylabel, fontsize=Font.LABEL)

        if chart_type == Chart.HUMIDITY:
            ax.set_ylim(0, 100)  # Humidity is always 0-100%

        ax.grid(True, alpha=chart_type.alpha)
        ax.set_facecolor(chart_type.facecolor)

        # Format x-axis
        self._format_time_axis(ax, timestamps)

        if measurements:
            self._add_stats(ax, measurements)

        # Add legend
        ax.legend(loc=chart_type.legend)

        fig.tight_layout()

        # Save using pathlib
        output_path = self._output_dir / chart_type.filename
        fig.savefig(output_path, dpi=chart_type.dpi, bbox_inches="tight")
        fig.clear()
        plt.close(fig)

    def _format_time_axis(self, ax: Axes, timestamps: list[datetime]):
        """Format the time axis for better readability."""
        if len(timestamps) > 1:
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d %H:%M"))
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())

            # Rotate labels for better readability
            for label in ax.get_xticklabels():
                label.set_rotation(45)
                label.set_horizontalalignment("right")

    def _add_stats(self, ax: Axes, measurements: list[float]):
        """Add temperature statistics text box to the axes."""
        avg_result = sum(measurements) / len(measurements)
        min_measurement = min(measurements)
        max_measurement = max(measurements)
        stats_text = f"Avg: {avg_result:.1f}°C\nMin: {min_measurement:.1f}°C\nMax: {max_measurement:.1f}°C"

        # position
        x, y = Stats.UPPER_RIGHT_CORNER

        ax.text(
            x,
            y,
            stats_text,
            transform=ax.transAxes,
            verticalalignment=Stats.VERTICAL_ALIGNMENT,
            horizontalalignment=Stats.HORIZONTAL_ALIGNMENT,
            bbox=dict(
                boxstyle=f"round,pad={Stats.PAD}",
                facecolor=Stats.FACECOLOR,
                alpha=Stats.ALPHA,
            ),
        )
