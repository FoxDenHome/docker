#!/bin/sh
set -e

cd "$(dirname "$0")"

rm -rf output && mkdir -p output

export DEFAULT_KERNEL_MODULES="8021q af_packet bridge dwc2 garp i2c-mux i2c-mux-pinctrl ipv6 llc pps-gpio pps-ldisc raspberrypi-hwmon roles rtc-pcf85063 stp"
export CMDLINE="console=tty1 root=/dev/root rootfstype=ext4 fsck.repair=yes ro rootwait"

docker pull ghcr.io/raspi-alpine/builder
docker run --rm -it -e DEFAULT_HOSTNAME=ntp -e ARCH=aarch64 -e DEFAULT_TIMEZONE=America/Los_Angeles -e CMDLINE -e DEFAULT_KERNEL_MODULES -e SIZE_ROOT_PART=1000M -e SIZE_ROOT_FS=400M -v $PWD/input:/input -v $PWD/output:/output ghcr.io/raspi-alpine/builder
