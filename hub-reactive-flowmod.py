# copy this file to ~/pox/pox/forwarding/ directory

# central point for pox API's
from pox.core import core

# import OpenFlow 1.0 modile & rename it "of"
import pox.openflow.libopenflow_01 as of

# display message
log = core.getLogger()

# handler function which specifies what to do when PacketIn happens
def _handle_PacketIn (event):

  # extract ethernet frame from event
  packet=event.parsed

  #create an insturction "msg" which will be used for adding flow table entry into device later on
  msg = of.ofp_flow_mod()

  # specify flood action
  msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))

  # send the instruction to device
  event.connection.send(msg)

# is used for for initializing pox component
def launch ():

  # specify handler function when PacketIn occurs
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)

  #display messages
  log.info("Hub application is running.")

