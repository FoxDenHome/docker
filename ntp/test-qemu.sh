#!/bin/sh
set -e

#docker build -t ghcr.io/doridian/raspi-alpine-builder ../../raspi-alpine-builder

./build.sh

cp output/sdcard.img.gz testimg/sdcard.img.gz
rm -f testimg/sdcard.img
gzip -d testimg/sdcard.img.gz
qemu-img resize testimg/sdcard.img 4G
docker run --rm -it --entrypoint=/bin/sh -v $PWD/testimg:/testimg ghcr.io/doridian/raspi-alpine-builder -c "cp /uboot/u-boot_rpi-64.bin /testimg/u-boot_rpi-64.bin"
qemu-system-aarch64 -M raspi3b -append 'console=ttyAMA0,115200 earlyprintk console=tty1 root=/dev/root rootfstype=ext4 fsck.repair=yes ro rootwait' -dtb testimg/bcm2710-rpi-3-b.dtb -kernel testimg/u-boot_rpi-64.bin -sd testimg/sdcard.img -m 1G -smp 4 -serial stdio
