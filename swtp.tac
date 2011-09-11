#!/usr/bin/env python
# -*- coding: utf-8 -*-
# You can run this .tac file directly with:
#    twistd -ny swtp.tac


from twisted.application import service, internet
from twisted.web import static, server

from ConfigParser import ConfigParser


import os
run_dir = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(run_dir, "config.ini")

def getWebService(config_path):
    """
    Return a service suitable for creating an application object.
    """
    
    if not config_path.startswith("/"):
        raise ValueError, "config_path must be a absolute path"

    config = ConfigParser()
    config.read(config_path)
    bind = config.get("webserver", "bind")
    port = int(config.get("webserver", "port"))
    public = config.get("webserver", "public")

    if not public.startswith("/"):
        public = os.path.join(os.path.dirname(config_path), public)

    # create a resource to serve static files

    fileServer = server.Site(static.File(public))
    return internet.TCPServer(8080, fileServer, interface=bind)

# this is the core part of any tac file, the creation of the root-level
# application object
application = service.Application("Stupid WebSocket TCP Proxy")

# attach the service to its parent application
service = getWebService(config_file)
service.setServiceParent(application)
