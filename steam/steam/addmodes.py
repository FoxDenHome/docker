#!/usr/bin/env python3
from subprocess import check_call, check_output
from re import sub
from os import environ

REFRESH_RATES = [60, 120]
RESOLUTIONS = [
    (1920, 1080),
    (2560, 1440),
    (2560, 1080),
    (3840, 1600),
]

biggest_resolution = max(RESOLUTIONS, key=lambda x: x[0] * x[1])
biggest_refresh = max(REFRESH_RATES)

def generate_modeline(resolution, refresh_rate):
    modeline = check_output(["cvt", str(resolution[0]), str(resolution[1]), str(refresh_rate)], encoding="utf-8").split("\n")[1].strip()
    return [x.strip("\r\n\t \"'") for x in sub("\\s+", " ",  modeline).split(" ")[1:]]

for resolution in RESOLUTIONS:
    for refresh_rate in REFRESH_RATES:
        modeline = generate_modeline(resolution, refresh_rate)
        print("Adding mode", modeline, flush=True)
        check_call(["xrandr", "--newmode"] + modeline)
        check_call(["xrandr", "--addmode", environ["VIDEO_PORT"], modeline[0]])
