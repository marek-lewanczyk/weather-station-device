#!/bin/zsh

# This script is used to deploy the device code to the device.

echo "🧹 Cleaning up existing files on device..."
mpremote fs rm -r :

echo "📦 Creating device catalogs..."

#!/bin/bash

echo "📦 Tworzenie katalogów na ESP32..."
mpremote fs mkdir sensors
mpremote fs mkdir collector
mpremote fs mkdir config
mpremote fs mkdir lib
mpremote fs mkdir utils

echo "📂 Wysyłanie plików..."
mpremote fs cp main.py :
mpremote fs cp weather_station.py :
mpremote fs cp sensors/bme680_sensor.py :sensors/
mpremote fs cp sensors/rain_sensor.py :sensors/
mpremote fs cp sensors/wind_speed_sensor.py :sensors/
mpremote fs cp sensors/as5600_sensor.py :sensors/
mpremote fs cp collector/weather_data_collector.py :collector/
mpremote fs cp config/config.json :config/
mpremote fs cp lib/bme680.py :lib/
mpremote fs cp utils/time_helpers.py :utils/
mpremote fs cp utils/wifi_manager.py :utils/

echo "🚀 Uruchamianie main.py..."
mpremote run main.py