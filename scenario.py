#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def customNet():

    net = Mininet(controller=Controller, switch=OVSSwitch)

    info( "*** Adding controller\n" )
    c0 = net.addController( 'c0', controller=Controller )

    info( "*** Adding switches\n" )
    s1 = net.addSwitch( 's1' )
    s2 = net.addSwitch( 's2' )
    s3 = net.addSwitch( 's3' )

    info( "*** Adding hosts\n" )
    h1 = net.addHost( 'h1' )
    h2 = net.addHost( 'h2' )
    h3 = net.addHost( 'h3' )
    h4 = net.addHost( 'h4' )
    h5 = net.addHost( 'h5' )
    h6 = net.addHost( 'h6' )
    h7 = net.addHost( 'h7' )
    h8 = net.addHost( 'h8' )
    h9 = net.addHost( 'h9' )

    info( "*** Adding links\n" )
    net.addLink( s1, h1 )
    net.addLink( s1, h2 )
    net.addLink( s2, h3 )
    net.addLink( s2, h4 )
    net.addLink( s2, h5 )
    net.addLink( s3, h6 )
    net.addLink( s3, h7 )
    net.addLink( s3, h8 )
    net.addLink( s3, h9 )

    info( "*** Starting network\n" )
    net.build()
    c0.start()
    s1.start( [c0] )
    s2.start( [c0] )
    s3.start( [c0] )

    info( "*** Running CLI\n" )
    CLI( net )

    info( "*** Stopping network\n" )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    customNet()
