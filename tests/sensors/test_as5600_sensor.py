import unittest
from unittest.mock import MagicMock
from datetime import datetime


def mock_format_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class MockI2C:
    def readfrom_mem(self, addr, memaddr, nbytes):
        return bytes([0x0C, 0x00])  # (0x0C << 8) | 0x00 = 3072


class AS5600Sensor:
    def __init__(self, scl_pin=22, sda_pin=21, north_deg=0):
        self.north_deg = north_deg
        self.i2c = MockI2C()
        self.address = 0x36

    def read_angle_raw(self):
        try:
            data = self.i2c.readfrom_mem(self.address, 0x0E, 2)
            angle = (data[0] << 8) | data[1]
            return angle
        except Exception:
            return None

    def read_degrees(self):
        raw = self.read_angle_raw()
        if raw is None:
            return None
        degrees = (raw * 360) / 4096
        corrected = (degrees - self.north_deg) % 360
        return round(corrected, 1)

    def angle_to_direction(self, angle):
        if angle >= 337.5 or angle < 22.5:
            return "N"
        elif angle < 67.5:
            return "NE"
        elif angle < 112.5:
            return "E"
        elif angle < 157.5:
            return "SE"
        elif angle < 202.5:
            return "S"
        elif angle < 247.5:
            return "SW"
        elif angle < 292.5:
            return "W"
        else:
            return "NW"

    def read(self):
        deg = self.read_degrees()
        if deg is not None:
            direction = self.angle_to_direction(deg)
            return {
                "wind_deg": deg,
                "wind_dir": direction
            }
        else:
            return {}


class TestAS5600Sensor(unittest.TestCase):
    def test_read_degrees_and_direction(self):
        sensor = AS5600Sensor(north_deg=0)
        result = sensor.read()
        self.assertEqual(result["wind_deg"], 270.0)
        self.assertEqual(result["wind_dir"], "W")

    def test_read_with_offset(self):
        sensor = AS5600Sensor(north_deg=90)
        result = sensor.read()
        self.assertEqual(result["wind_deg"], 180.0)
        self.assertEqual(result["wind_dir"], "S")

    def test_none_on_failure(self):
        class FailingI2C:
            def readfrom_mem(self, *args, **kwargs):
                raise Exception("I2C Failure")

        sensor = AS5600Sensor()
        sensor.i2c = FailingI2C()
        self.assertEqual(sensor.read(), {})


if __name__ == "__main__":
    unittest.main()