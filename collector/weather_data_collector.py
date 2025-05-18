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