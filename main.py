import uasyncio
from utils.wifi_manager import WifiManager
from weather_station import WeatherStation

async def main():
    wifi = WifiManager(ssid="WiFi_5", password="xakODlWwE")

    if not wifi.connect():
        print("❌ Brak połączenia z Wi-Fi. Koniec programu.")
        return

    station = WeatherStation()

    await uasyncio.gather(
        station.update(interval_ms=10),
        station.read_and_print(interval_sec=2),
        station.send_loop(interval_sec=10)
    )

uasyncio.run(main())