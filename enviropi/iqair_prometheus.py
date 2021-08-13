#!/usr/bin/python3 -u

from datetime import datetime
from urllib.request import urlopen
from time import sleep
from json import load
from prometheus_client import CollectorRegistry, REGISTRY, start_http_server
from prometheus_client.core import GaugeMetricFamily

URL = "https://website-api.airvisual.com/v1/stations/4d785ca890fb488c3bee"
PARAMS = "units.temperature=celsius&units.distance=km&units.pressure=millibar&AQI=US&language=en-US"

POLLUTANT_MAP = {
    'pm1':  '1.0',
    'pm25': '2.5',
    'pm10': '10',
}

REGISTRY = CollectorRegistry()

gauge_air_ug_per_m3 = GaugeMetricFamily('air_ug_per_m3', 'PM in ug/m3', labels=['size', 'environment'])
gauge_aqi = GaugeMetricFamily('aqi', 'AQI (US)')
gauge_pressure = GaugeMetricFamily('pressure', 'Pressure in millibar')
gauge_humidity = GaugeMetricFamily('humidity', 'Relative humidity in %')
gauge_temperature = GaugeMetricFamily('temperature', 'Temperature in Celsius')
gauge_wind_speed = GaugeMetricFamily('wind_speed', 'Wind speed in km/h')
gauge_wind_direction = GaugeMetricFamily('wind_direction', 'Wind direction in degrees')

class FakeCollector():
    def __init__(self):
        pass

    def collect(self):
        return [
            gauge_air_ug_per_m3,
            gauge_aqi,
            gauge_pressure,
            gauge_humidity,
            gauge_temperature,
            gauge_wind_speed,
            gauge_wind_direction,
        ]

REGISTRY.register(FakeCollector())

def load_station():
    data = load(urlopen("%s?%s" % (URL, PARAMS)))['current']

    dt = datetime.strptime(data['ts'], '%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp = dt.timestamp()

    gauge_aqi.add_metric([], data['aqi'], timestamp)
    gauge_pressure.add_metric([], data['pressure'], timestamp)
    gauge_humidity.add_metric([], data['humidity'], timestamp)
    gauge_temperature.add_metric([],data['temperature'], timestamp)

    gauge_wind_speed.add_metric([], data['wind']['speed'], timestamp)
    gauge_wind_direction.add_metric([], data['wind']['direction'], timestamp)

    for pollutant in data['pollutants']:
        gauge_air_ug_per_m3.add_metric([POLLUTANT_MAP[pollutant['pollutantName']], 'outside'], pollutant['concentration'], timestamp)

start_http_server(8003, registry=REGISTRY)

while True:
    print('Polling IQAir...')
    try:
        load_station()
    except Exception as e:
        print(e)
    sleep(60)
