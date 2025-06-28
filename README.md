# Pine A64 Temperature & Humidity Monitor 🌡️💧

A comprehensive monitoring system for the Pine A64 that reads temperature and humidity data from an I2C sensor, stores measurements in a database, generates visualizations, and sends email alerts when temperature thresholds are exceeded.

## 📋 Table of Contents

- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [System Architecture](#system-architecture)
- [Data Visualization](#data-visualization)
- [Alert System](#alert-system)
- [Database Schema](#database-schema)

## ✨ Features

- **Real-time Monitoring**: Continuous temperature and humidity measurements via I2C
- **Data Persistence**: SQLite database storage
- **Visual Analytics**: Automated chart generation with statistical summaries
- **Smart Alerts**: Email notifications when temperature drops below threshold
- **Professional Logging**: Comprehensive logging to both file and console
- **Modular Design**: Clean, object-oriented architecture for easy maintenance
- **Configuration Management**: External config file for email settings

## 🔧 Hardware Requirements

### Primary Components

- **Pine A64** (or compatible single-board computer)
- **Temperature/Humidity Sensor**: I2C-compatible sensor
- **Jumper Wires**: For I2C connections (SDA, SCL, VCC, GND)

### Wiring Diagram

```
Pine A64          Sensor
--------          ------
Pin 3 (SDA)   →   SDA
Pin 5 (SCL)   →   SCL
Pin 4 (3.3V)  →   5V
Pin 6 (GND)   →   GND
```

Based on the [Pine A64 Pi-2 Connector](https://files.pine64.org/doc/Pine%20A64%20Schematic/Pine%20A64%20Pin%20Assignment%20160119.pdf).

## 🚀 Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Gibirizon/pine64-temp-sensor.git
    cd pine64-temp-sensor
    ```

2. **Install dependencies:**

    ```bash
    uv sync
    ```

    Or for **pip** users:

    ```bash
    pip install -r requirements.txt
    ```

3. **Verify sensor connection:**
    ```bash
    sudo i2cdetect -y 0
    ```
    You should see your sensor at address `40`.

## ⚙️ Configuration

### Email Setup

Create a `config.ini` file in the project root:

```ini
[MAIL]
sender = your-email@gmail.com
password = your-app-password
server = smtp.gmail.com
port = 465
recipient = alert-recipient@gmail.com
```

### Configuration Parameters

The `config.py` file contains the following (and more) parameters:

| Parameter              | Description                          | Default |
| ---------------------- | ------------------------------------ | ------- |
| `i2c_bus`              | I2C bus number                       | `0`     |
| `device_address`       | Sensor I2C address                   | `0x40`  |
| `measurement_delay`    | Delay between measurements (seconds) | `0.5`   |
| `LOWER_TEMP_THRESHOLD` | Temperature alert threshold (°C)     | `1`     |

### Gmail Setup (Recommended)

1. Enable 2-factor authentication on your Google account
2. Generate an App Password: Google Account → Security → App passwords
3. Use the App Password in your `config.ini` file

## 🎯 Usage

### Basic Operation

```bash
# Run a single measurement cycle
python main.py -s config.ini
```

### Command Line Arguments

```bash
python main.py [OPTIONS]

Options:
  -s, --setup_file PATH  Configuration file path (required)
  -h, --help            Show help message
```

## 📁 Project Structure

```
pine-a64-monitor/
├── main.py                 # Entry point and CLI interface
├── config.ini              # Email configuration (create this)
├── requirements.txt        # Python dependencies
├── measurement.log         # Application logs
├── measurements.db         # SQLite database
├── charts/                 # Generated visualizations
│   ├── temperature.png
│   └── humidity.png
└── src/
    ├── __init__.py
    ├── measurement_system.py  # Main orchestration logic
    ├── database.py           # SQLAlchemy models and DB management
    ├── chart_generator.py    # Matplotlib chart generation
    ├── mailer.py            # Email notification system
    ├── email_templates.py   # HTML/text email templates
    └── config.py            # Configuration constants and dataclasses
```

### Core Components

- **MeasurementSystem**: Orchestrates the complete workflow
- **DatabaseManager**: Handles SQLite operations with context management
- **ChartGenerator**: Creates publication-quality matplotlib visualizations
- **Mailer**: Sends formatted email alerts with HTML templates

## 📊 Data Visualization

The system automatically generates two charts after each measurement:

### Chart Customization

Charts are configured via the `ChartConfig` dataclass in `src/config.py`:

## 🚨 Alert System

### Temperature Alerts

Automatic email notifications are sent when:

- Temperature drops below `LOWER_TEMP_THRESHOLD` (default: 1°C)
- Configurable threshold in `src/config.py`

Modify thresholds in `src/config.py` to change alert behavior:

```python
LOWER_TEMP_THRESHOLD = 1  # Change this value
```

## 🗄️ Database Schema

### Measurement Table

| Column        | Type     | Description                       |
| ------------- | -------- | --------------------------------- |
| `id`          | INTEGER  | Primary key (auto-increment)      |
| `temperature` | FLOAT    | Temperature in Celsius            |
| `humidity`    | FLOAT    | Relative humidity percentage      |
| `timestamp`   | DATETIME | Measurement time (auto-generated) |

## 🙏 Acknowledgments

- Pine64 community for hardware support
- SQLAlchemy team for excellent ORM
- Matplotlib developers for visualization tools
- smbus2 maintainers for I2C communication
