import time
from machine import Pin
from utils.time_helpers import format_timestamp

class RainSensor:
    def __init__(self, pin_number):
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.last_state = self.pin.value()
        self.count = 0

        self.mm_per_tip = 0.52615
        self.history = []  # lista (timestamp_ms, rain_mm)

        print(f"[{format_timestamp()}] [Rain] Initialized on pin {pin_number}")

    def update(self):
        current_state = self.pin.value()
        if current_state != self.last_state:
            self.count += 1
        self.last_state = current_state

    def read(self):
        tips = self.count
        rain_mm = round(tips * self.mm_per_tip, 2)
        self.count = 0

        now = time.ticks_ms()
        self.history.append((now, rain_mm))

        # usuń wpisy starsze niż godzina
        one_hour_ms = 60 * 60 * 1000
        self.history = [
            (ts, val) for (ts, val) in self.history
            if time.ticks_diff(now, ts) <= one_hour_ms
        ]

        total_rain = round(sum(val for (_, val) in self.history), 2)

        # print(f"[{format_timestamp()}] [Rain] Tips: {tips}, Rain: {rain_mm} mm, Total (1h): {total_rain} mm")

        return {
            "rain_tips": tips,
            "rain_mm": rain_mm,
            "rain_mm_total": total_rain
        }