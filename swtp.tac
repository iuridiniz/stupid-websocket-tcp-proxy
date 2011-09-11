#!/usr/bin/env python
# -*- coding: utf-8 -*-
# You can run this .tac file directly with:
#    twistd -ny swtp.tac

from twisted.application import service

from lib.webserver import getWebServer

import os
run_dir = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(run_dir, "config.ini")

# this is the core part of any tac file, the creation of the root-level
# application object
application = service.Application("Stupid WebSocket TCP Proxy")

# attach the service to its parent application
service = getWebServer(config_file).getService()

service.setServiceParent(application)
