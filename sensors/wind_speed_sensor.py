from machine import Pin
from utils.time_helpers import format_timestamp
import time

class WindSpeedSensor:
    def __init__(self, pin_number, pulses_per_rotation, radius_cm):
        self.pin = Pin(pin_number, Pin.IN)
        self.last_state = self.pin.value()
        self.pulse_count = 0
        self.last_read_time = time.ticks_ms()
        self.pulses_per_rotation = pulses_per_rotation
        self.radius_cm = radius_cm

    def update(self):
        current_state = self.pin.value()
        if current_state != self.last_state:
            # print(f"[WindSpeed] State change: {self.last_state} → {current_state}")
            self.pulse_count += 1
            self.last_state = current_state

    def read(self):
        now = time.ticks_ms()
        elapsed_ms = time.ticks_diff(now, self.last_read_time)
        elapsed_sec = elapsed_ms / 1000.0

        pulses = self.pulse_count
        self.pulse_count = 0
        self.last_read_time = now

        rotation_count = pulses / self.pulses_per_rotation
        if elapsed_sec > 0:
            rps = rotation_count / elapsed_sec
        else:
            rps = 0

        circumference_m = 2 * 3.1416 * (self.radius_cm / 100)
        m_per_sec = rps * circumference_m
        km_per_hour = m_per_sec * 3.6

        print(f"[{format_timestamp()}] [WindSpeed] Pulses: {pulses}, Speed: {km_per_hour:.2f} km/h")

        return {
            "wind_pulses": pulses,
            "wind_kmph": round(km_per_hour, 2),
            "wind_mps": round(m_per_sec, 2)
        }


