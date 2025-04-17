# wifi.py

import network
import time
import config
from device.utils import debug_log


def connect_to_wifi(timeout: int = 20):
    """
    Connects to Wi-Fi using credentials from config.py.

    :param timeout:
    :return: True if connected, False otherwise.
    """

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        debug_log("Already connected: " + str(wlan.ifconfig()))

    debug_log("Connecting to Wi-Fi...")

    wlan.connect(config.WIFI_SSID, config.WIFI_PASSWORD)

    for i in range(timeout):
        if wlan.isconnected():
            break
        debug_log("Waiting... ({i + 1}s)")
        time.sleep(1)

    if wlan.isconnected():
        debug_log("Connected to Wi-Fi: " + str(wlan.ifconfig()))
        return True
    else:
        debug_log("Wi-Fi connection failed.")
        return False