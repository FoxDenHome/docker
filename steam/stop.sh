#!/bin/bash
set -xeuo pipefail

docker stop steam_steam-headless_1 || true

export DISPLAY=':0'
/usr/lib/xorg/Xorg vt8 -config /opt/docker/steam/xorg.conf -noreset -novtswitch -sharevts -dpi 96 +extension GLX +extension RANDR +extension RENDER +extension MIT-SHM "$DISPLAY" &
sleep 1

nvidia-settings -a 'GPUMemoryTransferRateOffsetAllPerformanceLevels=0' -a '[gpu:0]/GPUFanControlState=0'
nvidia-settings -q 'GPUMemoryTransferRateOffsetAllPerformanceLevels' -q '[gpu:0]/GPUFanControlState'
nvidia-smi -pm 0

sleep 1

killall Xorg
wait
