#!/bin/sh

ssh router '/system/backup/save dont-encrypt=yes name=router.backup'
scp router:/router.backup ./
ssh router '/file/remove router.backup'

ssh router '/export file=router.rsc show-sensitive'
scp router:/router.rsc ./
ssh router '/file/remove router.rsc'


