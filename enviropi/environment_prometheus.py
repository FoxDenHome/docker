#!/usr/bin/env python3

from bme280 import bme280, bme280_i2c
#import ltr559
from enviroplus import gas
from prometheus_client import Gauge, start_http_server
from time import sleep

#BME 280 sensor
bme280_i2c.set_default_bus(1)
bme280_i2c.set_default_i2c_address(0x76)
bme280.setup()
def bme280_sample():
	return bme280.read_all()

gauge_temperature = Gauge('temperature', 'Temperature in Celsius')
gauge_humidity = Gauge('humidity', 'Relative humidity in %')
gauge_pressure = Gauge('pressure', 'Pressure in hPa')

def poll_bme280():
	data = bme280_sample()
	temperature = data.temperature
	humidity = data.humidity
	pressure = data.pressure

	gauge_temperature.set(temperature)
	gauge_humidity.set(humidity)
	gauge_pressure.set(pressure)

# ltr559 sensor
#gauge_lux = Gauge('lux', 'Light level (lux)')
#gauge_proxmity = Gauge('proximity', 'Proximity')

#def poll_ltr559():
#	lux = ltr559.get_lux()
#	prox = ltr559.get_proximity()
#
#	gauge_lux.set(lux)
#	gauge_proxmity.set(prox)

# GAS sensor
gauge_gas_kohm = Gauge('gas_kohm', 'Concentration of gas', ['type'])

def poll_gas():
	gas_readings = gas.read_all()

	gauge_gas_kohm.labels(type='reducing').set(gas_readings.reducing)
	gauge_gas_kohm.labels(type='oxidizing').set(gas_readings.oxidising)
	gauge_gas_kohm.labels(type='nh3').set(gas_readings.nh3)

start_http_server(8001)

INTERVAL = 1.0

print("Starting poll sequence every %f seconds" % INTERVAL)

while True:
	print("Poll run!")
	poll_bme280()
	poll_gas()
	#poll_ltr559()
	print("Poll end!")
	sleep(INTERVAL)
