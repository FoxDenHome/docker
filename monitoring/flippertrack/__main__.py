from prometheus_client import CollectorRegistry, REGISTRY, start_http_server
from prometheus_client.core import GaugeMetricFamily
from requests import get
from time import sleep
from re import compile as re_compile, escape as re_escape
from dateutil.parser import parse as dateutil_parse

URL = "https://ship.flipp.dev/"
TEMPLATE_URL = "https://raw.githubusercontent.com/flipperdevices/ship-flipp/main/index.tmpl"
QUERY_PERIOD = 60

REGISTRY = CollectorRegistry()
FLIPPER_GAUGE = GaugeMetricFamily(
    'flipper_shipping', 'Number of shipping flippers', labels=['state'])


class FakeCollector():
    def __init__(self):
        pass

    def collect(self):
        return [
            FLIPPER_GAUGE,
        ]


REGISTRY.register(FakeCollector())

SHIPPED_FLIPPERS_REGEX = None
DELIVERED_FLIPPERS_REGEX = None
DATE_REGEX = None


def extractRegexFromLine(line, match):
    if match not in line:
        return None

    line = line.strip()

    regex = line.replace(match, "___VARIABLE___")
    regex = re_escape(regex)
    regex = regex.replace("___VARIABLE___", "([^<>]+)")

    regex_compiled = re_compile(f"^{regex}$")
    print(regex_compiled)
    return regex_compiled


def extractRegexFromTemplate():
    global SHIPPED_FLIPPERS_REGEX
    global DELIVERED_FLIPPERS_REGEX
    global DATE_REGEX

    tpl = get(TEMPLATE_URL).text
    for line in tpl.splitlines():
        regex = extractRegexFromLine(line, "{{ .status.Total }}")
        if regex is not None:
            SHIPPED_FLIPPERS_REGEX = regex
        regex = extractRegexFromLine(line, "{{ .status.Delivered }}")
        if regex is not None:
            DELIVERED_FLIPPERS_REGEX = regex
        regex = extractRegexFromLine(
            line, "{{ .status.Date.Format \"January 02 15:04 MST\" }}")
        if regex is not None:
            DATE_REGEX = regex


def returnIfMatch(line, regex):
    match = regex.match(line)
    if match is not None:
        return match[1]
    return None


def setGauge(state, value):
    FLIPPER_GAUGE.labels(state=state).set(value)


def checkStats():
    query_date = None
    query_shipped = None
    query_delivered = None

    stats = get(URL).text
    for line in stats.splitlines():
        line = line.strip()

        match = returnIfMatch(line, SHIPPED_FLIPPERS_REGEX)
        if match is not None:
            query_shipped = int(match, 10)
        match = returnIfMatch(line, DELIVERED_FLIPPERS_REGEX)
        if match is not None:
            query_delivered = int(match, 10)
        match = returnIfMatch(line, DATE_REGEX)
        if match is not None:
            query_date = dateutil_parse(match)

    if not query_date or not query_shipped or not query_delivered:
        return

    timestamp = query_date.timestamp()

    FLIPPER_GAUGE.samples = []
    FLIPPER_GAUGE.add_metric(['shipped'], query_shipped, timestamp)
    FLIPPER_GAUGE.add_metric(
        ['in_transit'], query_shipped - query_delivered, timestamp)
    FLIPPER_GAUGE.add_metric(['delivered'], query_delivered, timestamp)

    print("Q", query_date, "S", query_shipped, "D", query_delivered)

if __name__ == "__main__":
    extractRegexFromTemplate()
    start_http_server(8888, registry=REGISTRY)
    while True:
        try:
            checkStats()
        except Exception as e:
            print(e)
        sleep(QUERY_PERIOD)
