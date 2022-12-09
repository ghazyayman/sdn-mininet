# improt class "Mininet" from "net" package 
from mininet.net import Mininet

# import class "CLI" from "cli" package
from mininet.cli import CLI

# create object "net" from Mininet class
net=Mininet()

# add host "h1", "h2", "h3", &  "h4" to blueprint "net"
h1=net.addHost('h1')
h2=net.addHost('h2')
h3=net.addHost('h3')
h4=net.addHost('h4')

# add switch "s1" to topology blueprint "net"
s1=net.addSwitch('s1')

# add controller  "c0" to topology blueprint "net"
c0=net.addController('c0')

# add links between hosts "h1, h2, h3, h4" & switch
net.addLink(h1,s1)
net.addLink(h2,s1)
net.addLink(h3,s1)
net.addLink(h4,s1)

# start the network consisting of 4 hosts, 1 switch & 1 controller
net.start()

# set ip addresses from "172.24.0.1" to "172.24.0.4"
h1.setIP('172.24.0.1/16')
h2.setIP('172.24.0.2/16')
h3.setIP('172.24.0.3/16')
h4.setIP('172.24.0.4/16')

print ("host h1 has IP address",h1.IP())
print ("host h2 has IP address",h2.IP())
print ("host h3 has IP address",h3.IP())
print ("host h4 has IP address",h4.IP())

print("ping test between host h1 nad h2")
print (h1.cmd('ping -c2',h2.IP()))

# provides command line interface for the created network
CLI(net)

# stop (dismantle) the network 
net.stop()
