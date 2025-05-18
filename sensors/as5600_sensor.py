import time
from machine import I2C, Pin
from utils.time_helpers import format_timestamp

class AS5600Sensor:
    def __init__(self, scl_pin=22, sda_pin=21, north_deg=0):
        self.north_deg = north_deg
        self.i2c = self.initialize_i2c(scl_pin, sda_pin)
        self.address = 0x36

        if self.i2c:
            print(f"[{format_timestamp()}] [WindDir] Sensor initialized")
        else:
            print(f"[{format_timestamp()}] [WindDir] Initialization failed")

    def initialize_i2c(self, scl_pin, sda_pin):
        try:
            print(f"[{format_timestamp()}] [WindDir] Initialized I2C on pins SCL: {scl_pin}, SDA: {sda_pin}")
            return I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin))
        except Exception as e:
            print(f"[{format_timestamp()}] [WindDir] Error initializing I2C: {e}")
            return None

    def read_angle_raw(self):
        try:
            data = self.i2c.readfrom_mem(self.address, 0x0E, 2)
            angle = (data[0] << 8) | data[1]
            return angle
        except Exception as e:
            print(f"[{format_timestamp()}] [WindDir] Error reading raw angle: {e}")
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
            print(f"[{format_timestamp()}] [WindDir] Direction: {deg}° → {direction}")
            return {
                "wind_deg": deg,
                "wind_dir": direction
            }
        else:
            print(f"[{format_timestamp()}] [WindDir] No direction read")
            return {}