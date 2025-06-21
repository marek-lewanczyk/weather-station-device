import unittest
from datetime import datetime


def mock_format_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class MockBME680:
    def __init__(self, i2c, address=0x77):
        self.temperature = 24.6
        self.humidity = 55.3
        self.pressure = 1012.8
        self.gas = 12345.6


class BME680Sensor:
    def __init__(self, scl_pin=22, sda_pin=21):
        self.i2c = True
        self.bme680 = MockBME680(self.i2c)

    def read(self):
        try:
            data = {
                "temperature": round(self.bme680.temperature, 1),
                "humidity": round(self.bme680.humidity, 1),
                "pressure": round(self.bme680.pressure, 1),
                "gas": round(self.bme680.gas)
            }
            return data
        except Exception:
            return None


class TestBME680Sensor(unittest.TestCase):
    def test_sensor_readings(self):
        sensor = BME680Sensor()
        result = sensor.read()
        self.assertEqual(result["temperature"], 24.6)
        self.assertEqual(result["humidity"], 55.3)
        self.assertEqual(result["pressure"], 1012.8)
        self.assertEqual(result["gas"], 12346)


if __name__ == "__main__":
    unittest.main()