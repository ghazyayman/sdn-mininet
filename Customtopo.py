""" 
Custom topology creation for routing example.
"""
from mininet.topo import Topo

class MyTopo( Topo ):

    def __init__( self ):

        "Create custom topo."
    
        #Initialize topology
        Topo.__init__( self )
    
        # Add hosts and switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
    
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')

        #Add links
        self.addLink(s1, s4)
        self.addLink(s1, s5)
        self.addLink(s1, s2)
        self.addLink(s2, h2)
        self.addLink(s2, h2)

        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s1)

topos = { 'mytopo': ( lambda: MyTopo() ) }


locations = {'c0':(50,50), 's1':(200,300), 's2':(600,300), 's3':(400,100),'h1':(200,450),'h2':(600,450)}

