#!/bin/bash -e

if [ -z "$NVIDIA_DRIVER_VERSION" ]; then
    exit 1
fi

cd /tmp

# If version is different, new installer will overwrite the existing components
if [ ! -f "/tmp/NVIDIA-Linux-x86_64-$NVIDIA_DRIVER_VERSION.run" ]; then
    # Check multiple sources in order to probe both consumer and datacenter driver versions
    curl -fsL -O "https://us.download.nvidia.com/XFree86/Linux-x86_64/$NVIDIA_DRIVER_VERSION/NVIDIA-Linux-x86_64-$NVIDIA_DRIVER_VERSION.run" || curl -fsL -O "https://us.download.nvidia.com/tesla/$NVIDIA_DRIVER_VERSION/NVIDIA-Linux-x86_64-$NVIDIA_DRIVER_VERSION.run" || { echo "Failed NVIDIA GPU driver download. Exiting."; exit 1; }
fi

# Extract installer before installing
sh "NVIDIA-Linux-x86_64-$NVIDIA_DRIVER_VERSION.run" -x
cd "NVIDIA-Linux-x86_64-$NVIDIA_DRIVER_VERSION"
# Run installation without the kernel modules and host components
./nvidia-installer --silent \
                --no-kernel-module \
                --install-compat32-libs \
                --no-nouveau-check \
                --no-nvidia-modprobe \
                --no-rpms \
                --no-backup \
                --no-check-for-alternate-installs
rm -rf /tmp/NVIDIA*
