
from pox.core import core
from pox.lib.addresses import IPAddr, EthAddr
import pox.openflow.libopenflow_01 as of

class Switch:
  def __init__ (self, connection):
    self.connection = connection
    self.macToPort = {}

    connection.addListeners(self)

  def _handle_PacketIn (self, event):
    in_port=event.port
    dpid=event.dpid
   
    packet = event.parsed
    eth = packet.find("ethernet")
    self.macToPort[eth.src]=in_port
    if eth.dst in self.macToPort:
	out_port=self.macToPort[eth.dst]
    else:
	out_port=of.OFPP_FLOOD
    
    # install flow entry into device
    if out_port!=of.OFPP_FLOOD:
    	    msg = of.ofp_flow_mod()
	    msg.match = of.ofp_match()
	    msg.match.dl_dst=eth.dst
	    msg.match.in_port=event.port
	    msg.idle_timeout = 10
	    msg.hard_timeout = 30
	    msg.actions.append(of.ofp_action_output(port = out_port))
 	    self.connection.send(msg)

      # create an instruction "msg" for sending packet out
    else:
  	msg = of.ofp_packet_out()
  	msg.actions.append(of.ofp_action_output(port = out_port))
    	msg.data = event.ofp 
    	self.connection.send(msg)

def _handle_ConnectionUp (event):

  # handler function which specifies what to do when ConnectionUp happens
    Switch(event.connection)

  # is used for initializing pox component
def launch ():
  # specify handler function when ConnectionUp
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
