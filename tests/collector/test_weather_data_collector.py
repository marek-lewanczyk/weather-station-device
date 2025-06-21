import unittest


class MockSensor:
    def __init__(self, name, data, should_fail=False):
        self.name = name
        self.data = data
        self.should_fail = should_fail
        self.updated = False

    def read(self):
        if self.should_fail:
            raise Exception("Sensor read error")
        return self.data

    def update(self):
        if self.should_fail:
            raise Exception("Sensor update error")
        self.updated = True


class WeatherDataCollector:
    def __init__(self, sensors):
        self.sensors = sensors

    def read_all(self):
        data = {}
        for sensor in self.sensors:
            if hasattr(sensor, "read"):
                try:
                    data.update(sensor.read())
                except Exception as e:
                    print(f"[WeatherDataCollector] Error reading from {sensor.__class__.__name__}: {e}")
        return data

    def update_all(self):
        for sensor in self.sensors:
            if hasattr(sensor, "update"):
                try:
                    sensor.update()
                except Exception as e:
                    print(f"[WeatherDataCollector] Error updating {sensor.__class__.__name__}: {e}")


class TestWeatherDataCollector(unittest.TestCase):
    def test_read_all_success(self):
        sensors = [
            MockSensor("SensorA", {"temp": 22.5}),
            MockSensor("SensorB", {"humidity": 50})
        ]
        collector = WeatherDataCollector(sensors)
        result = collector.read_all()
        self.assertEqual(result, {"temp": 22.5, "humidity": 50})

    def test_read_with_failing_sensor(self):
        sensors = [
            MockSensor("SensorA", {"temp": 22.5}),
            MockSensor("FailingSensor", {}, should_fail=True)
        ]
        collector = WeatherDataCollector(sensors)
        result = collector.read_all()
        self.assertEqual(result, {"temp": 22.5})

    def test_update_all(self):
        s1 = MockSensor("SensorA", {"x": 1})
        s2 = MockSensor("SensorB", {"y": 2})
        collector = WeatherDataCollector([s1, s2])
        collector.update_all()
        self.assertTrue(s1.updated)
        self.assertTrue(s2.updated)

    def test_update_with_failing_sensor(self):
        s1 = MockSensor("SensorA", {"x": 1})
        s2 = MockSensor("FailingSensor", {}, should_fail=True)
        collector = WeatherDataCollector([s1, s2])
        collector.update_all()
        self.assertTrue(s1.updated)


if __name__ == "__main__":
    unittest.main()