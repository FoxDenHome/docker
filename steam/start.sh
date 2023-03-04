#!/bin/bash
set -xeuo pipefail

docker stop steam_steam-headless_1 || true

docker update steam_steam-headless_1 --cpuset-mems=1

export DISPLAY=':0'
/usr/lib/xorg/Xorg vt8 -config /opt/docker/steam/xorg.conf -noreset -novtswitch -sharevts -dpi 96 +extension GLX +extension RANDR +extension RENDER +extension MIT-SHM "$DISPLAY" &
sleep 1

nvidia-smi -pm 1
nvidia-settings -a 'GPUMemoryTransferRateOffsetAllPerformanceLevels=1000' -a 'GPUFanControlState=0' -a 'GPUTargetFanSpeed=0'
sleep 0.1
nvidia-settings -a 'GPUMemoryTransferRateOffsetAllPerformanceLevels=1000' -a 'GPUFanControlState=1' -a 'GPUTargetFanSpeed=100'
sleep 0.1
nvidia-settings -q 'GPUMemoryTransferRateOffsetAllPerformanceLevels' -q 'GPUFanControlState' -q 'GPUCurrentFanSpeed' -q 'GPUTargetFanSpeed'
sleep 0.1

killall Xorg
wait

systemctl stop superfan

docker start steam_steam-headless_1 || true
