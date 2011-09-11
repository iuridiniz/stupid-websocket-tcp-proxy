#!/usr/bin/env python
# -*- coding: utf-8 -*-
# You can run this .tac file directly with:
#    twistd -ny swtp.tac


from twisted.application import service, internet
from twisted.web import static
from twisted.protocols.portforward import ProxyFactory

from lib.websocket import WebSocketHandler, WebSocketSite, WebSocketFactory

from ConfigParser import SafeConfigParser as ConfigParser


import os
run_dir = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(run_dir, "config.ini")

def getWebService(config_path):
    """
    Return a service suitable for creating an application object.
    """
    
    if not config_path.startswith("/"):
        raise ValueError, "config_path must be an absolute path"

    config = ConfigParser()
    config.read(config_path)
    bind = config.get("webserver", "bind")
    port = int(config.get("webserver", "port"))
    public = config.get("webserver", "public")

    if not public.startswith("/"):
        public = os.path.join(os.path.dirname(config_path), public)

    # create a resource to serve static files
    root = static.File(public)
    web_server = WebSocketSite(root)

    # setup proxies
    for url, dest in config.items('url-maps'):
        tcp_host, tcp_port = dest.split(':')
        proxy = ProxyFactory(tcp_host, int(tcp_port))
        ws = WebSocketFactory(proxy)
        web_server.addHandler(url, ws.buildHandler)

    return internet.TCPServer(port, web_server, interface=bind)

# this is the core part of any tac file, the creation of the root-level
# application object
application = service.Application("Stupid WebSocket TCP Proxy")

# attach the service to its parent application
service = getWebService(config_file)
service.setServiceParent(application)
