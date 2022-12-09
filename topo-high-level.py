# import class "Topo" from "topo" package
from mininet.topo import Topo
from mininet.net import Mininet

# import classes "Mininet" & "CLI" from "net" & "cli" package
from mininet.cli import CLI

# create child class "OneSwitchTopo" from "Topo" parent class
class SingleSwitchTopo(Topo):

	# build network from topology object
	def __init__(self,count=1):

		# add hosts loop
		Topo.__init__(self)
		hosts=[self.addHost('h%d' %i)
			for i in range(1,count+1)]

			# add switch "s1"
		s1=self.addSwitch('s1')

		# add links bettween hosts & switch loop
		for host in hosts:
			self.addLink(host,s1)

# create network according to OneSwitchTopo(4) specifications
net=Mininet(topo=SingleSwitchTopo(4))

# get host names of hosts "h1,h2,h3,h4"
h1,h2,h3,h4=net.get('h1','h2','h3','h4')

#set ip addresses from "172.24.0.1" to "172.24.0.4"
h1.setIP('172.24.0.1/16')	
h2.setIP('172.24.0.2/16')	
h3.setIP('172.24.0.3/16')	
h4.setIP('172.24.0.4/16')
print("host h1 has IP address",h1.IP())	
print("host h2 has IP address",h2.IP())	
print("host h3 has IP address",h3.IP())	
print("host h4 has IP address",h4.IP())	

# start the network consisting of 4 hosts, 1 switch & 1 controller
net.start()

print("ping test between host h1 and h2")
print (h1.cmd('ping -c2',h2.IP()))

# provides command line interface for the created network 
CLI(net)

# stop (dismantle) the network
net.stop()
