#!/bin/sh

ssh router '/system/backup/save dont-encrypt=yes name=router.backup'
ssh router '/export file=router.rsc show-sensitive'

sleep 1

scp router:/router.backup router:/router.rsc ./
if [ ! -z "$1" ]
then
    cp router.backup router.rsc "$1"
fi

sleep 1

ssh router '/file/remove router.backup'
ssh router '/file/remove router.rsc'
