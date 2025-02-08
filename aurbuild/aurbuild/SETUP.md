# Shell

```sh
sudo pacman-key --recv-key 723AB072D36DF76677DA5ACF41ADC5FF876838A8
sudo pacman-key --lsign-key 723AB072D36DF76677DA5ACF41ADC5FF876838A8
```

# `/etc/pacman.conf`

```
[foxdenaur]
Server = https://archlinux.foxden.network/other/foxdenaur
SigLevel = Required TrustedOnly
```
