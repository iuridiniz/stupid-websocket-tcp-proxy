#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2011 Iuri Gomes Diniz. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
# 
#    1. Redistributions of source code must retain the above copyright notice, this list of
#       conditions and the following disclaimer.
# 
#    2. Redistributions in binary form must reproduce the above copyright notice, this list
#       of conditions and the following disclaimer in the documentation and/or other materials
#       provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY Iuri Gomes Diniz ''AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation are those of the
# authors and should not be interpreted as representing official policies, either expressed
# or implied, of Iuri Gomes Diniz.

import os

from ConfigParser import SafeConfigParser as ConfigParser

from twisted.protocols.portforward import ProxyFactory
from twisted.application import internet
from twisted.web import static

from websocket import WebSocketSite, WebSocketFactory

__author__      = "Iuri Gomes Diniz"
__copyright__   = "Copyright 2011, Iuri Gomes Diniz"
__credits__     = ["Iuri Diniz"]
__license__     = "Simplified BSD License"
__version__     = "0.1"
__maintainer__  = "Iuri Diniz"
__email__       = "iuridiniz@gmail.com"
__status__      = "Development"

__all__ = ["WebServer", "getWebServer"]


class WebServer(WebSocketSite):
    def __init__(self, root, port=8080, interface='localhost'):
        WebSocketSite.__init__(self, root)
        
        self._port = port
        self._interface = interface

    def getService(self):
        return internet.TCPServer(self._port, self, interface=self._interface)

def getWebServer(config_path):
    """
    Return a service suitable for creating an application object.
    """

    if not config_path.startswith("/"):
        raise ValueError, "config_path must be a absolute path"

    config = ConfigParser()
    config.read(config_path)
    bind = config.get("webserver", "bind")
    port = int(config.get("webserver", "port"))
    root_path = config.get("webserver", "root")

    if not root_path.startswith("/"):
        root_path = os.path.join(os.path.dirname(config_path), root_path)

    # create a resource to serve static files
    root = static.File(root_path)
    web_server = WebServer(root, port, bind)

    # setup proxies
    for url, dest in config.items('url-maps'):
        tcp_host, tcp_port = dest.split(':')
        proxy = ProxyFactory(tcp_host, int(tcp_port))
        ws = WebSocketFactory(proxy)
        web_server.addHandler(url, ws.buildHandler)

    return web_server

if __name__ == "__main__":
    pass
