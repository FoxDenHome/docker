#!/bin/sh
set -e

DEST="$1"

sftp -b /dev/stdin "$DEST" <<EOF
put output/sdcard_update.img.gz /tmp/sdcard_update.img.gz
put output/sdcard_update.img.gz.sha256 /tmp/sdcard_update.img.gz.sha256
EOF

ssh -t "$DEST" 'sudo -n /bin/sh -l -c "ab_flash /tmp/sdcard_update.img.gz && reboot"'
