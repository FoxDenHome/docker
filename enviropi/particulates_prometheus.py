#!/usr/bin/env python3

from pms5003 import PMS5003
from prometheus_client import Gauge, start_http_server

pms5003 = None

def make_pms5003():
	global pms5003
	pms5003 = PMS5003(device='/dev/ttyAMA0')

make_pms5003()

gauge_air_ug_per_m3 = Gauge('air_ug_per_m3', 'PM in ug/m3', ['size', 'environment'])
gauge_air_per_1l = Gauge('air_per_1l', 'Number of particles > X um in 0.1L air', ['size'])

start_http_server(8002)

print("Begin readings cycle...")

while True:
	particulate_readings = pms5003.read()
	print("Got readings!")

	gauge_air_ug_per_m3.labels(size=1.0, environment='normal').set(particulate_readings.pm_ug_per_m3(1.0, False))
	gauge_air_ug_per_m3.labels(size=2.5, environment='normal').set(particulate_readings.pm_ug_per_m3(2.5, False))
	gauge_air_ug_per_m3.labels(size=10, environment='normal').set(particulate_readings.pm_ug_per_m3(10, False))
	gauge_air_ug_per_m3.labels(size=1.0, environment='atmospheric').set(particulate_readings.pm_ug_per_m3(1.0, True))
	gauge_air_ug_per_m3.labels(size=2.5, environment='atmospheric').set(particulate_readings.pm_ug_per_m3(2.5, True))
	gauge_air_ug_per_m3.labels(size=10, environment='atmospheric').set(particulate_readings.pm_ug_per_m3(None, True))

	gauge_air_per_1l.labels(size=0.3).set(particulate_readings.pm_per_1l_air(0.3))
	gauge_air_per_1l.labels(size=0.5).set(particulate_readings.pm_per_1l_air(0.5))
	gauge_air_per_1l.labels(size=1.0).set(particulate_readings.pm_per_1l_air(1.0))
	gauge_air_per_1l.labels(size=2.5).set(particulate_readings.pm_per_1l_air(2.5))
	gauge_air_per_1l.labels(size=5.0).set(particulate_readings.pm_per_1l_air(5.0))
	gauge_air_per_1l.labels(size=10).set(particulate_readings.pm_per_1l_air(10))

