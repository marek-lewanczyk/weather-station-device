import time
from machine import I2C, Pin
from lib import bme680
from utils.time_helpers import format_timestamp

class BME680Sensor:
    def __init__(self, scl_pin=22, sda_pin=21):
        self.i2c = self.initialize_i2c(scl_pin, sda_pin)
        self.bme680 = self.initialize_sensor()

        if self.i2c and self.bme680:
            print(f"[{format_timestamp()}] [BME680] Sensor initialized")
        else:
            print(f"[{format_timestamp()}] [BME680] Initialization failed")

    def initialize_i2c(self, scl_pin, sda_pin):
        try:
            print(f"[{format_timestamp()}] [BME680] Initialized I2C on pins SCL: {scl_pin}, SDA: {sda_pin}")
            return I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
        except Exception as e:
            print(f"[{format_timestamp()}] [BME680] Error initializing I2C: {e}")
            return None

    def initialize_sensor(self):
        try:
            print(f"[{format_timestamp()}] [BME680] Initialized BME680 sensor: address 0x77")
            return bme680.BME680_I2C(self.i2c, address=0x77)
        except Exception as e:
            print(f"[{format_timestamp()}] [BME680] Error initializing BME680 sensor: {e}")
            return None

    def read(self):
        try:
            data = {
                "temperature": round(self.bme680.temperature, 1),
                "humidity": round(self.bme680.humidity, 1),
                "pressure": round(self.bme680.pressure, 1),
                "gas": round(self.bme680.gas)
            }
            return data
        except Exception as e:
            print(f"[{format_timestamp()}] [BME680] Error reading sensor data: {e}")
            return None