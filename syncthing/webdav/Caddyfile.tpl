{
	order webdav before file_server
}

__SYNCTHING_DOMAIN__ {
	root * /syncthing
	file_server {
		browse
		hide .stfolder
	}
	rewrite /dav /dav/
	webdav /dav/* {
		prefix /dav
	}
	basicauth {
		doridian {$WEBDAV_PASSWORD_DORIDIAN}
	}
}
