import unittest


class MockWLAN:
    def __init__(self):
        self.active_state = False
        self.connected = False
        self.connection_attempts = 0
        self.config = ("192.168.1.123", "255.255.255.0", "192.168.1.1", "8.8.8.8")

    def active(self, state=None):
        if state is None:
            return self.active_state
        self.active_state = state

    def isconnected(self):
        self.connection_attempts += 1
        return self.connected

    def connect(self, ssid, password):
        self.connected = True

    def ifconfig(self):
        return self.config


class WifiManager:
    def __init__(self, ssid: str, password: str, timeout: int = 30):
        self.ssid = ssid
        self.password = password
        self.timeout = timeout
        self.wlan = MockWLAN()
        self.wlan.active(True)

    def is_connected(self) -> bool:
        return self.wlan.isconnected()

    def connect(self) -> bool:
        if self.is_connected():
            self.get_ip()
            return True

        self.wlan.connect(self.ssid, self.password)

        for _ in range(self.timeout):
            if self.is_connected():
                return True
        return False

    def get_ip(self) -> str:
        if self.is_connected():
            return self.wlan.ifconfig()[0]
        return "Not connected"


class TestWifiManager(unittest.TestCase):
    def test_initial_state_not_connected(self):
        manager = WifiManager("SSID", "PASS")
        manager.wlan.connected = False
        self.assertFalse(manager.is_connected())

    def test_connect_success(self):
        manager = WifiManager("SSID", "PASS")
        result = manager.connect()
        self.assertTrue(result)
        self.assertEqual(manager.get_ip(), "192.168.1.123")

    def test_get_ip_when_disconnected(self):
        manager = WifiManager("SSID", "PASS")
        manager.wlan.connected = False
        self.assertEqual(manager.get_ip(), "Not connected")


if __name__ == "__main__":
    unittest.main()