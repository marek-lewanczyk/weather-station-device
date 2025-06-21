import unittest


class MockPin:
    IN = 0

    def __init__(self, pin_number, mode):
        self._state = 1

    def value(self):
        return self._state

    def set_state(self, val):
        self._state = val


class WindSpeedSensor:
    def __init__(self, pin_number, pulses_per_rotation, radius_cm):
        self.pin = MockPin(pin_number, MockPin.IN)
        self.last_state = self.pin.value()
        self.pulse_count = 0
        self.last_read_time = 0
        self.pulses_per_rotation = pulses_per_rotation
        self.radius_cm = radius_cm
        self.mock_time = 0

    def mock_ticks_ms(self):
        return self.mock_time

    def advance_time(self, ms):
        self.mock_time += ms

    def update(self):
        current_state = self.pin.value()
        if current_state != self.last_state:
            self.pulse_count += 1
        self.last_state = current_state

    def read(self):
        now = self.mock_ticks_ms()
        elapsed_ms = now - self.last_read_time
        elapsed_sec = elapsed_ms / 1000.0

        pulses = self.pulse_count
        self.pulse_count = 0
        self.last_read_time = now

        rotation_count = pulses / self.pulses_per_rotation
        rps = rotation_count / elapsed_sec if elapsed_sec > 0 else 0

        circumference_m = 2 * 3.1416 * (self.radius_cm / 100)
        m_per_sec = rps * circumference_m
        km_per_hour = m_per_sec * 3.6

        return {
            "wind_pulses": pulses,
            "wind_kmph": round(km_per_hour, 2),
            "wind_mps": round(m_per_sec, 2)
        }


class TestWindSpeedSensor(unittest.TestCase):
    def test_wind_speed_measurement(self):
        sensor = WindSpeedSensor(pin_number=4, pulses_per_rotation=2, radius_cm=9)
        sensor.pin.set_state(0)
        sensor.update()
        sensor.pin.set_state(1)
        sensor.update()
        sensor.pin.set_state(0)
        sensor.update()
        sensor.pin.set_state(1)
        sensor.update()
        sensor.advance_time(1000)

        result = sensor.read()
        self.assertEqual(result["wind_pulses"], 4)
        self.assertGreater(result["wind_kmph"], 0)
        self.assertGreater(result["wind_mps"], 0)


if __name__ == "__main__":
    unittest.main()