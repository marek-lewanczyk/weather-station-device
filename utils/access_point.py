import network
from utils.time_helpers import format_timestamp

class AccessPointManager:
    def __init__(self, ssid="ESP_Weather_Station", password="", hidden=False):
        self.ssid = ssid
        self.password = password
        self.hidden = hidden
        self.ap = network.WLAN(network.AP_IF)
        self.start()
        print(f"[{format_timestamp()}] [Access Point] Access Point started: {self.ssid} (IP: {ip}) (Password: {'set' if self.password else 'not set'})")

    def start(self):
        self.ap.active(True)
        self.ap.config(
            essid=self.ssid,
            password=self.password,
            authmode=network.AUTH_OPEN if self.password == "" else network.AUTH_WPA_WPA2_PSK,
            hidden=self.hidden
        )
        while not self.ap.active():
            pass

        ip = self.ap.ifconfig()[0]
        return ip