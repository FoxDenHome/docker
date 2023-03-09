#!/usr/bin/env python3

from subprocess import check_call, check_output, SubprocessError
from re import sub
from os import getenv
from argparse import ArgumentParser
from dataclasses import dataclass

REFRESH_RATES = [60, 75, 90, 100, 120, 144]
RESOLUTIONS = [
    (1920, 1080),
    (2560, 1440),
    (2560, 1080),
    (3840, 1600),
    (3840, 2160),
]

@dataclass(frozen=True, eq=True)
class Mode:
    width: int
    height: int
    refresh_rate: int = 60

    @property
    def modeline(self) -> list[str]:
        cvt_output = check_output(["cvt", str(self.width), str(self.height), str(self.refresh_rate)], encoding="utf-8").split("\n")[1].strip()
        modeline_split = [x.strip("\r\n\t \"'") for x in sub("\\s+", " ",  cvt_output).split(" ")[1:]]
        return [self.name] + modeline_split[1:]

    @property
    def name(self) -> str:
        return f"{self.width}x{self.height}_{self.refresh_rate}"

    def add(self, port: str) -> None:
        print("Adding mode", self.name, "to port", port, flush=True)
        check_call(["xrandr", "--newmode"] + self.modeline)
        check_call(["xrandr", "--addmode", port, self.name])

    def switch(self, port: str, add: bool = False) -> None:
        if add:
            try:
                self.add(port=port)
            except SubprocessError:
                pass

        print("Switching to mode", self.name, "on port", port, flush=True)
        check_call(["xrandr", "--output", port, "--mode", self.name])

def add_defaults(port: str) -> None:
    for resolution in RESOLUTIONS:
        for refresh_rate in REFRESH_RATES:
            mode = Mode(width=resolution[0], height=resolution[1], refresh_rate=refresh_rate)
            mode.add(port=port)

def main() -> None:
    parser = ArgumentParser(description="Add custom modes to xrandr and switch to them. Call with --defaults to add some defaults")
    parser.add_argument("--defaults", help="Add some default modes", default=False, action="store_true")
    parser.add_argument("--width", "-x", help="Width of the mode", type=int, default=0)
    parser.add_argument("--height", "-y", help="Height of the mode", type=int, default=0)
    parser.add_argument("--refresh-rate", "-r", help="Refresh rate of the mode", type=int, default=60)
    parser.add_argument("--port", "-p", help="Which video port to use", type=str, default=getenv("VIDEO_PORT", ""))
    parser.add_argument("--switch", "-s", help="Switch to the mode after it was added", default=False, action="store_true")

    args = parser.parse_args()

    if args.defaults:
        add_defaults(args.port)
        return

    mode = Mode(width=args.width, height=args.height, refresh_rate=args.refresh_rate)
    if args.switch:
        mode.switch(add=True, port=args.port)
    else:
        mode.add(port=args.port)

if __name__ == "__main__":
    main()
