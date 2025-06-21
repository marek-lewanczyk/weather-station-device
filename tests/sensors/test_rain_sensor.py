import unittest
from datetime import datetime


def mock_format_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class MockPin:
    IN = 0
    PULL_UP = 1

    def __init__(self, pin_number, mode, pull):
        self._state = 1
        self.pin_number = pin_number

    def value(self):
        return self._state

    def set_state(self, val):
        self._state = val


class RainSensor:
    def __init__(self, pin_number):
        self.pin = MockPin(pin_number, MockPin.IN, MockPin.PULL_UP)
        self.last_state = self.pin.value()
        self.count = 0
        self.mm_per_tip = 0.52615
        self.history = []

    def update(self):
        current_state = self.pin.value()
        if current_state != self.last_state:
            self.count += 1
        self.last_state = current_state

    def read(self):
        tips = self.count
        rain_mm = round(tips * self.mm_per_tip, 2)
        self.count = 0

        now = 0
        self.history.append((now, rain_mm))

        one_hour_ms = 60 * 60 * 1000
        self.history = [
            (ts, val) for (ts, val) in self.history
            if now - ts <= one_hour_ms
        ]

        total_rain = round(sum(val for (_, val) in self.history), 2)

        return {
            "rain_tips": tips,
            "rain_mm": rain_mm,
            "rain_mm_total": total_rain
        }


class TestRainSensor(unittest.TestCase):
    def test_tip_counting(self):
        sensor = RainSensor(pin_number=5)

        sensor.pin.set_state(0)
        sensor.update()
        sensor.pin.set_state(1)
        sensor.update()

        result = sensor.read()

        self.assertEqual(result["rain_tips"], 2)
        self.assertAlmostEqual(result["rain_mm"], round(2 * 0.52615, 2))
        self.assertAlmostEqual(result["rain_mm_total"], result["rain_mm"])


if __name__ == "__main__":
    unittest.main()