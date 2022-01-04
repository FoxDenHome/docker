#!/bin/bash
set -e

# Configure boot process
mkenvimage -s 0x4000 -o "$BOOTFS_PATH/uboot.env" "$INPUT_PATH/uboot.env"
cp "$INPUT_PATH/usercfg.txt" "$BOOTFS_PATH/usercfg.txt"
echo 'include usercfg.txt' >> "$BOOTFS_PATH/config.txt"

# Install packages
chroot_exec apk update
chroot_exec apk upgrade
chroot_exec apk add bridge-utils curl screen prometheus-node-exporter gpsd gpsd-clients chrony bridge wget sudo tcpdump nano openssh-sftp-server ethtool keepalived keepalived-openrc

# Configure services
chroot_exec rc-update del ntpd default
chroot_exec rc-update del ab_clock default
chroot_exec rc-update add gpsd
chroot_exec rc-update add chronyd
chroot_exec rc-update add node-exporter
chroot_exec rc-update add hwclock
chroot_exec rc-update add keepalived

# Configure kernel modules
echo -n > "$ROOTFS_PATH/etc/modules"
for mod in ${DEFAULT_KERNEL_MODULES}
do
    echo "$mod" >> "$ROOTFS_PATH/etc/modules"
done
echo 'Loading the following modules:'
cat "$ROOTFS_PATH/etc/modules"
echo 'END OF MODULE LIST'

# Add additional tmpfs entries
echo >> "$ROOTFS_PATH/etc/fstab"
add_tmpfs() {
    TMP_PATH="$1"
    mkdir -p "$ROOTFS_PATH/$TMP_PATH"
    echo "tmpfs $TMP_PATH tmpfs defaults 0 0" >> "$ROOTFS_PATH/etc/fstab"
}
add_tmpfs '/var/log'

# Undo things the image creator did we don't want
revert_data_ln() {
    LN_PATH="$1"
    rm -f "$ROOTFS_PATH/$LN_PATH" || rmdir "$ROOTFS_PATH/$LN_PATH"
    mv "$DATAFS_PATH/$LN_PATH" "$ROOTFS_PATH/$LN_PATH"
}
revert_data_override() {
    LN_PATH="$1"
    rm -f "$ROOTFS_PATH/$LN_PATH" || rmdir "$ROOTFS_PATH/$LN_PATH"
    mv "$ROOTFS_PATH/${LN_PATH}_org" "$ROOTFS_PATH/$LN_PATH"
}
revert_data_ln '/etc/hostname'
revert_data_ln '/etc/network/interfaces'
sed 's~/data/etc/~/tmp/~g' -i "$ROOTFS_PATH/etc/udhcpc/udhcpc.conf"
revert_data_ln '/etc/localtime'
revert_data_ln '/etc/timezone'
revert_data_ln '/etc/shadow'
revert_data_ln '/root'
revert_data_override '/etc/conf.d/dropbear'

# Copy our rootfs additions
cp -rp "$INPUT_PATH/rootfs/"* "$ROOTFS_PATH"

IMAGE_COMMIT="$(cat "$ROOTFS_PATH/etc/image_commit")"
IMAGE_DATE="$(cat "$ROOTFS_PATH/etc/image_date")"
sed "s/__IMAGE_COMMIT__/$IMAGE_COMMIT/" -i "$ROOTFS_PATH/etc/motd"
sed "s/__IMAGE_DATE__/$IMAGE_DATE/" -i "$ROOTFS_PATH/etc/motd"

# Add users
chroot_exec addgroup sudo

add_user() {
    ADDUSER="$1"
    chroot_exec adduser -D "$ADDUSER"
    chroot_exec adduser "$ADDUSER" sudo

    chroot_exec mkdir -p "/home/$ADDUSER/.ssh"
    wget "https://raw.githubusercontent.com/Doridian/home-scripts/master/sshkeys/$ADDUSER" -O "$ROOTFS_PATH/home/$ADDUSER/.ssh/authorized_keys"
    chroot_exec chmod -R 600 "/home/$ADDUSER/.ssh"
    chroot_exec chmod 700 "/home/$ADDUSER" "/home/$ADDUSER/.ssh"
    chroot_exec chown -R "$ADDUSER:$ADDUSER" "/home/$ADDUSER"
}

add_user doridian
add_user wizzy
