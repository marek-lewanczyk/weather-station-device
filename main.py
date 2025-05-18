import uasyncio

from weather_station import WeatherStation

async def main():
    station = WeatherStation()

    await uasyncio.gather(
        station.update(interval_ms=10),
        station.read_and_print(interval_sec=2)
    )

uasyncio.run(main())