from pox.core import core
# Import "IPAddr" & "ETHAddr" class
from pox.lib.addresses import IPAddr, EthAddr
import pox.openflow.libopenflow_01 as of
import os

class Switch:
  def __init__ (self, connection):
    self.connection = connection
	# Initialize macToPort Dictionary
    self.macToPort = {}

    connection.addListeners(self)

  def _handle_PacketIn (self, event):
	# extract port from event & store it in variable
    in_port=event.port
	# extract dpid from event & store it in variable
    dpid=event.dpid
	# extract frame from event & store it in variable
    packet = event.parsed
	# extract ethernet header 
    eth = packet.find("ethernet")
	#insert entry based on source mac into dictionary 
    self.macToPort[eth.src]=in_port
	# if destination mac is in  dictionary, then send packet to corresponding port otherwise flood
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
	    msg.data = event.ofp 
 	    self.connection.send(msg)
	#create an instruction "msg" for sending packet out
    else:
  	msg = of.ofp_packet_out()
  	msg.actions.append(of.ofp_action_output(port = out_port))
    	msg.data = event.ofp 
    	self.connection.send(msg)

#handler function which specifies what to do when ConnectionUp happens
def _handle_ConnectionUp (event):
    
    policyFile = "%s/pox/pox/forwarding/firewall-mac-policies.csv" % os.environ['HOME']
    rules_file = open(policyFile,"r")
    rules=[rule.strip()for rule in rules_file]
    for i in range(len(rules)):
	rule_list=rules[i].split(' ')
	fw_add_rule=of.ofp_flow_mod()
	fw_add_rule.match=of.ofp_match()
	fw_add_rule.match.dl_src=EthAddr(rule_list[0])
	fw_add_rule.match.dl_dst=EthAddr(rule_list[1])
	event.connection.send(fw_add_rule)
	
    Switch(event.connection)

def launch ():
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
