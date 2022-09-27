""" A Testing module for SDN Lab03
Use Mininet as underlying network topology, Floodlight as remote controller.
Construct a two-layer tree topology and manually build up switch flow table
entries for basic forwarding without Floodlight-provided forwarding module.
"""

from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topolib import TreeTopo
from mininet.log import setLogLevel
from mininet.cli import CLI

import time

class TwoLayerTreeTopo(object):
    """ Build up a two-layer tree topology
                                dpid:1
                                +----+
                       +--------+ s1 +-------+
                       |      p1+----+p2     |
                       |p3                 p3|
                     +----+               +----+
                     | s2 |dpid:2   dpid:3| s3 |
                     +----+               +----+
                    p1| |p2              p1| |p2
                +-----+ +---+          +---+ +---+
                |           |          |         |
              +-+--+        |        +-+--+      |
              | h1 |        |        | h3 |      |
              +----+        |        +----+      |
        00:00:00:00:00:01   |  00:00:00:00:00:03 |
                         +--+-+                +-+--+
                         | h2 |                | h4 |
                         +----+                +----+
                   00:00:00:00:00:02     00:00:00:00:00:04
    """

    def __init__(self, controller_ip, controller_port):
        self.controller_ip = controller_ip
        self.controller_port = controller_port
        self.tree = TreeTopo(depth=2, fanout=2)

        # Some important arguments:
        # - autoSetMacs=True: set MAC addrs automatically like IP addresses
        # - listenPort=6634 (optional): base listening port to open
        self.net = Mininet(topo=self.tree,
                           controller=None,
                           autoSetMacs=True,
                           listenPort=6634)
        self.net.addController('floodlight',
                               controller=RemoteController,
                               ip=self.controller_ip,
                               port=self.controller_port)
        self.sw = self.net.switches

    def kick_start(self):
        """ Fire up mininet with customized topology and settings
        """
        self.net.start()
        self.net.waitConnected()

    def build_table(self):
        """ Construct switches' flow table
        """
        # For ARP request
        self.sw[0].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:01,dl_dst=ff:ff:ff:ff:ff:ff,idle_timeout=0,actions=output:2')
        self.sw[0].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:02,dl_dst=ff:ff:ff:ff:ff:ff,idle_timeout=0,actions=output:2')
        self.sw[0].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:03,dl_dst=ff:ff:ff:ff:ff:ff,idle_timeout=0,actions=output:1')
        self.sw[0].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:04,dl_dst=ff:ff:ff:ff:ff:ff,idle_timeout=0,actions=output:1')

        self.sw[1].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:01,dl_dst=ff:ff:ff:ff:ff:ff,idle_timeout=0,actions=output:2,3')
        self.sw[1].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:02,dl_dst=ff:ff:ff:ff:ff:ff,idle_timeout=0,actions=output:1,3')
        self.sw[1].dpctl('add-flow', 'in_port=3,dl_src=00:00:00:00:00:03,dl_dst=ff:ff:ff:ff:ff:ff,idle_timeout=0,actions=output:1,2')
        self.sw[1].dpctl('add-flow', 'in_port=3,dl_src=00:00:00:00:00:04,dl_dst=ff:ff:ff:ff:ff:ff,idle_timeout=0,actions=output:1,2')

        self.sw[2].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:03,dl_dst=ff:ff:ff:ff:ff:ff,idle_timeout=0,actions=output:2,3')
        self.sw[2].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:04,dl_dst=ff:ff:ff:ff:ff:ff,idle_timeout=0,actions=output:1,3')
        self.sw[2].dpctl('add-flow', 'in_port=3,dl_src=00:00:00:00:00:01,dl_dst=ff:ff:ff:ff:ff:ff,idle_timeout=0,actions=output:1,2')
        self.sw[2].dpctl('add-flow', 'in_port=3,dl_src=00:00:00:00:00:02,dl_dst=ff:ff:ff:ff:ff:ff,idle_timeout=0,actions=output:1,2')

        # For ICMP request/reply and ARP reply
        self.sw[0].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:03,idle_timeout=0,actions=output:2')
        self.sw[0].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:04,idle_timeout=0,actions=output:2')
        self.sw[0].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04,idle_timeout=0,actions=output:2')
        self.sw[0].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:03,idle_timeout=0,actions=output:2')
        self.sw[0].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:01,idle_timeout=0,actions=output:1')
        self.sw[0].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:02,idle_timeout=0,actions=output:1')
        self.sw[0].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:02,idle_timeout=0,actions=output:1')
        self.sw[0].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01,idle_timeout=0,actions=output:1')

        self.sw[1].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02,idle_timeout=0,actions=output:2')
        self.sw[1].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:03,idle_timeout=0,actions=output:3')
        self.sw[1].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04,idle_timeout=0,actions=output:3')
        self.sw[1].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01,idle_timeout=0,actions=output:1')
        self.sw[1].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:03,idle_timeout=0,actions=output:3')
        self.sw[1].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:04,idle_timeout=0,actions=output:3')
        self.sw[1].dpctl('add-flow', 'in_port=3,dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:01,idle_timeout=0,actions=output:1')
        self.sw[1].dpctl('add-flow', 'in_port=3,dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:02,idle_timeout=0,actions=output:2')
        self.sw[1].dpctl('add-flow', 'in_port=3,dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01,idle_timeout=0,actions=output:1')
        self.sw[1].dpctl('add-flow', 'in_port=3,dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:02,idle_timeout=0,actions=output:2')

        self.sw[2].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:01,idle_timeout=0,actions=output:3')
        self.sw[2].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:02,idle_timeout=0,actions=output:3')
        self.sw[2].dpctl('add-flow', 'in_port=1,dl_src=00:00:00:00:00:03,dl_dst=00:00:00:00:00:04,idle_timeout=0,actions=output:2')
        self.sw[2].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:01,idle_timeout=0,actions=output:3')
        self.sw[2].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:02,idle_timeout=0,actions=output:3')
        self.sw[2].dpctl('add-flow', 'in_port=2,dl_src=00:00:00:00:00:04,dl_dst=00:00:00:00:00:03,idle_timeout=0,actions=output:1')
        self.sw[2].dpctl('add-flow', 'in_port=3,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:03,idle_timeout=0,actions=output:1')
        self.sw[2].dpctl('add-flow', 'in_port=3,dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:04,idle_timeout=0,actions=output:2')
        self.sw[2].dpctl('add-flow', 'in_port=3,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:03,idle_timeout=0,actions=output:1')
        self.sw[2].dpctl('add-flow', 'in_port=3,dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:04,idle_timeout=0,actions=output:2')

    def show_table(self):
        """ Dump the switch flow table
        """
        print ('FLOW TABLES')
        for i in self.sw:
            print ('*** switch %x ***') % int(i.dpid, 16)
            print (i.dpctl('dump-flows'))

    def ping_test(self):
        """ Ping all for connectivity test
        """
        self.net.pingAll()

    def __del__(self):
        self.net.stop()

def main():
    """ Main procedure
    Assume the Floodlight controller without forwarding module is listening at
    loopback interface and port 6633, which is the default port.
    """
    topo = TwoLayerTreeTopo('127.0.0.1', 6633)
    topo.kick_start()
    topo.build_table()
    topo.show_table()
    topo.ping_test()

if __name__ == '__main__':
    setLogLevel('info')
    main()