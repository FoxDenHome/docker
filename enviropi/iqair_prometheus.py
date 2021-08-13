#!/usr/bin/python3 -u

from urllib.request import urlopen
from time import sleep
from json import load
from prometheus_client import Gauge, start_http_server

URL = "https://website-api.airvisual.com/v1/stations/4d785ca890fb488c3bee"
PARAMS = "units.temperature=celsius&units.distance=km&units.pressure=millibar&AQI=US&language=en-US"

POLLUTANT_MAP = {
    'pm1':  1.0,
    'pm25': 2.5,
    'pm10': 10,
}

gauge_air_ug_per_m3 = Gauge('air_ug_per_m3', 'PM in ug/m3', ['size', 'environment'])
gauge_aqi = Gauge('aqi', 'AQI (US)')
gauge_pressure = Gauge('pressure', 'Pressure in millibar')
gauge_humidity = Gauge('humidity', 'Relative humidity in %')
gauge_temperature = Gauge('temperature', 'Temperature in Celsius')

gauge_wind_speed = Gauge('wind_speed', 'Wind speed in km/h')
gauge_wind_direction = Gauge('wind_direction', 'Wind direction in degrees')

def load_station():
    data = load(urlopen("%s?%s" % (URL, PARAMS)))['current']

    gauge_aqi.set(data['aqi'])
    gauge_pressure.set(data['pressure'])
    gauge_humidity.set(data['humidity'])
    gauge_temperature.set(data['temperature'])

    gauge_wind_speed.set(data['wind']['speed'])
    gauge_wind_direction.set(data['wind']['direction'])

    for pollutant in data['pollutants']:
        gauge_air_ug_per_m3.labels(size=POLLUTANT_MAP[pollutant['pollutantName']], environment='outside').set(pollutant['concentration'])

start_http_server(8003)

while True:
    print('Polling IQAir...')
    try:
        load_station()
    except Exception as e:
        print(e)
    sleep(60000)
