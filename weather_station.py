from sensors.wind_speed_sensor import WindSpeedSensor
from sensors.rain_sensor import RainSensor
from sensors.bme680_sensor import BME680Sensor
from sensors.as5600_sensor import AS5600Sensor
from collector.weather_data_collector import WeatherDataCollector
from utils.time_helpers import format_timestamp
import uasyncio
import urequests

class WeatherStation:
    def __init__(self):
        self.bme680 = BME680Sensor()
        self.rain_sensor = RainSensor(19)
        self.wind_speed_sensor = WindSpeedSensor(18, 1, 8.5)
        self.AS5600_sensor = AS5600Sensor()
        self.collector = WeatherDataCollector([self.bme680, self.rain_sensor, self.wind_speed_sensor, self.AS5600_sensor])
        self.api_url = "http://192.168.1.104:8000/weather/"

    async def update(self, interval_ms=10):
        while True:
            self.collector.update_all()
            await uasyncio.sleep_ms(interval_ms)

    async def read_and_print(self, interval_sec=2):
        while True:
            data = self.collector.read_all()
            if data:
                print(f"[{format_timestamp()}] [WeatherStation] "
                      f"Temp: {data['temperature']}°C, Hum: {data['humidity']}%, "
                      f"Pressure: {data['pressure']} hPa, Gas: {data['gas']} Ω, "
                      f"Rain (last 1h): {data['rain_mm_total']} mm, "
                      f"Rain (last read): {data['rain_mm']} mm, "
                      f"Rain (tips): {data['rain_tips']}, "
                      f"Wind Speed: {data['wind_kmph']} km/h, "
                      f"Wind Speed (m/s): {data['wind_mps']}, "
                      f"Wind Pulses: {data['wind_pulses']}, "
                      f"Wind Dir: {data['wind_deg']}° ({data['wind_dir']})" )
            else:
                print(f"[{format_timestamp()}] [WeatherStation] No data collected")
            await uasyncio.sleep(interval_sec)

    def send_to_server(self, data):
        try:
            headers = {"Content-Type": "application/json"}
            res = urequests.post(self.api_url, json=data, headers=headers)
            print(f"[{format_timestamp()}] ✅ Sent to server: {res.status_code}")
            res.close()
        except Exception as e:
            print(f"[{format_timestamp()}] ❌ Failed to send data: {e}")

    async def send_loop(self, interval_sec=60):
        while True:
            data = self.collector.read_all()
            if data:
                self.send_to_server(data)
            await uasyncio.sleep(interval_sec)