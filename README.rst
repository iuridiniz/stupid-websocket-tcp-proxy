==================================
Stupid WebSocket TCP Proxy (SWTP)
==================================

**A very stupid WebSocket server in order to proxy TCP connections**

Requirements:

* python
* twisted

It exposes an existing service over WebSocket, so a javascript application can communicate 
with desired service. *It's necessary to use some implentation of the service protocol over WebSocket.*

Quick start::

    $ cp config.ini.sample config.ini
    $ twistd -n -y swtp.tac
    $ xdg-open http://localhost:9091/examples/


Configuring
-----------
See ``config.ini.sample``


Available Protocols
-------------------

Stomp:
  Provided by http://jmesnil.net/stomp-websocket/doc/


Writing a new protocol
----------------------
TODO
