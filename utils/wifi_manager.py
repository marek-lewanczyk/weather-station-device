import network
import time

class WifiManager:
    def __init__(self, ssid: str, password: str, timeout: int = 30):
        self.ssid = ssid
        self.password = password
        self.timeout = timeout
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def is_connected(self) -> bool:
        """Check if the device is connected to WiFi."""
        return self.wlan.isconnected()

    def connect(self) -> bool:
        """Connect to the WiFi network."""
        if self.is_connected():
            self.get_ip()
            print("Already connected to WiFi.")
            return True

        print(f"Connecting to WiFi SSID: {self.ssid}")
        self.wlan.connect(self.ssid, self.password)

        start_time = time.time()
        while not self.is_connected():
            if time.time() - start_time > self.timeout:
                print("Connection timed out.")
                return False
            time.sleep(1)

        print("Connected to WiFi:", self.wlan.ifconfig())
        return True

    def get_ip(self) -> str:
        """Get the IP address of the connected WiFi."""
        if self.is_connected():
            print("Current IP address:", self.wlan.ifconfig()[0])
            return self.wlan.ifconfig()[0]
        else:
            return "Not connected"