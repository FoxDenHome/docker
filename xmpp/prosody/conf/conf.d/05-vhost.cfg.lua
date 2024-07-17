-- XEP-0368: SRV records for XMPP over TLS
-- https://compliance.conversations.im/test/xep0368/
legacy_ssl_ssl = {
	certificate = "certs/foxden.network.crt";
	key = "certs/foxden.network.key";
}
legacy_ssl_ports = { 5223 }

-- https://prosody.im/doc/certificates#service_certificates
-- https://prosody.im/doc/ports#ssl_configuration
https_ssl = {
	certificate = "certs/foxden.network.crt";
	key = "certs/foxden.network.key";
}

local _slidge_priv = {
  roster = "both";
  message = "outgoing";
  iq = {
    ["http://jabber.org/protocol/pubsub"] = "both";
    ["http://jabber.org/protocol/pubsub#owner"] = "set";
  };
}

VirtualHost "foxden.network"
  disco_items = {
    { "upload.xmpp.foxden.network" },
  }
  privileged_entities = {
    ["telegram.xmpp.foxden.network"] = _slidge_priv,
    ["discord.xmpp.foxden.network"] = _slidge_priv,
  }

-- Dummy VHost to allow Slidge to function for some reason
VirtualHost "xmpp.foxden.network"
  allow_registration = false
  privileged_entities = {
    ["telegram.xmpp.foxden.network"] = _slidge_priv,
    ["discord.xmpp.foxden.network"] = _slidge_priv,
  }

-- Set up a http file upload because proxy65 is not working in muc
Component "upload.xmpp.foxden.network" "http_file_share"
	http_file_share_expires_after = 60 * 60 * 24 * 7 -- a week in seconds
	local size_limit = 1024 * 1024 * 1000 -- 1000MB
	http_file_share_size_limit = size_limit
	http_file_share_daily_quota = 10 * size_limit -- 10x the size limit

Component "muc.xmpp.foxden.network" "muc"
	name = "Prosody Chatrooms"
	restrict_room_creation = false
	max_history_messages = 20
	modules_enabled = {
		"muc_mam",
		"vcard_muc"
	}

-- Set up a SOCKS5 bytestream proxy for server-proxied file transfers
Component "proxy.xmpp.foxden.network" "proxy65"
	proxy65_address = "proxy.xmpp.foxden.network"
	proxy65_acl = { "foxden.network" }

-- Implements a XEP-0060 pubsub service.
Component "pubsub.xmpp.foxden.network" "pubsub"
