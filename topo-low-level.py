
from mininet.node import OVSSwitch,Host,Controller

# import classes from "node" & "link" package
from mininet.link import Link

# create host "h1" 
h1=Host('h1')
h2=Host('h2')
h3=Host('h3')
h4=Host('h4')

# create switch "s1" in root namespace
s1=OVSSwitch('s1',inNamespace=False)

# create controller "c0" in root namespace
c0=Controller('c0',inNamespace=False)

# create link between host "h1" & switch "s1"
Link(h1,s1)
Link(h2,s1)
Link(h3,s1)
Link(h4,s1)

# set ip to "172.24.0.1"
h1.setIP('172.24.0.1/16')
h2.setIP('172.24.0.2/16')
h3.setIP('172.24.0.3/16')
h4.setIP('172.24.0.4/16')

#start controller
c0.start()

# connect switch "s1" with controller "c0"
s1.start([c0])

# display ip of host "h1"
print("host h1 has IP address",h1.IP())
print("host h2 has IP address",h2.IP())
print("host h3 has IP address",h3.IP())
print("host h4 has IP address",h4.IP())
print("ping test between host h1 and h2")

# perform ping test between host "h1" & "h2"
print h1.cmd('ping -c2',h2.IP())

# stop switch "s1"
s1.stop()

#stop controller
c0.stop()
