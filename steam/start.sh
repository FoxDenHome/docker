#!/bin/bash
set -xeuo pipefail

docker stop steam_steam-headless_1 || true

export DISPLAY=':0'
/usr/lib/xorg/Xorg vt8 -config /opt/docker/steam/xorg.conf -noreset -novtswitch -sharevts -dpi 96 +extension GLX +extension RANDR +extension RENDER +extension MIT-SHM "$DISPLAY" &
sleep 1

nvidia-smi -pm 1
nvidia-settings -a 'GPUMemoryTransferRateOffsetAllPerformanceLevels=1000' -a '[gpu:0]/GPUFanControlState=1' -a '[fan:0]/GPUCurrentFanSpeed=100'
nvidia-settings -q 'GPUMemoryTransferRateOffsetAllPerformanceLevels' -q '[gpu:0]/GPUFanControlState' -q '[fan:0]/GPUCurrentFanSpeed'

sleep 1

killall Xorg
wait

docker start steam_steam-headless_1 || true
