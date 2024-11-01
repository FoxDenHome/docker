# Shell

```sh
sudo pacman-key --recv-key 459B9477FCE9B8CD889DFFC2C55F467DFDC3DFC8
sudo pacman-key --lsign-key 459B9477FCE9B8CD889DFFC2C55F467DFDC3DFC8
```

# `/etc/pacman.conf`

```
[foxdenaur]
Server = https://archlinux.foxden.network/other/foxdenaur
SigLevel = Required TrustedOnly
```
