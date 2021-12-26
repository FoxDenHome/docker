#!/bin/bash
set -e

DEVB=enp131s0f0
DEV="${DEVB}np0"
MAC_PREFIX="00:16:3E:CA:7E"
NUM_VFS="$(cat "/sys/class/net/$DEV/device/sriov_totalvfs")"

echo 1 > "/sys/class/net/$DEV/device/sriov_drivers_autoprobe"

echo "$NUM_VFS" > "/sys/class/net/$DEV/device/sriov_numvfs"
for i in `seq 0 $((NUM_VFS - 1))`
do
	MAC="$MAC_PREFIX:$(printf "%02x" "$i")"
	echo "Configuring VF $i ($MAC)"
	ip link set dev "$DEV" vf "$i" mac "$MAC" mtu 9000
	ip link set dev "${DEVB}v${i}" address "$MAC" mtu 9000 || true
done
echo 'Done!'
