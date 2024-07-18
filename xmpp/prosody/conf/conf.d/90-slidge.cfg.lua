component_ports = { 5347 }
component_interfaces = { "0.0.0.0" }

Component "discord.xmpp.foxden.network"
  component_secret = os.getenv("SLIDCORD_SECRET")
  modules_enabled = {"isolate_host", "privilege", "discoitems"}
  disco_items = {
    { "pubsub.xmpp.foxden.network" },
    { "upload.xmpp.foxden.network" },
    { "muc.xmpp.foxden.network" },
    { "foxden.network" },
  }
  isolate_except_domains = {"foxden.network", "xmpp.foxden.network", "upload.xmpp.foxden.network"}

Component "telegram.xmpp.foxden.network"
  component_secret = os.getenv("SLIDGRAM_SECRET")
  modules_enabled = {"isolate_host", "privilege", "discoitems"}
  disco_items = {
    { "pubsub.xmpp.foxden.network" },
    { "upload.xmpp.foxden.network" },
    { "muc.xmpp.foxden.network" },
    { "foxden.network" },
  }
  isolate_except_domains = {"foxden.network", "xmpp.foxden.network", "upload.xmpp.foxden.network"}
