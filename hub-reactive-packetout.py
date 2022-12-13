# Import "core" which act as a central point for pox components
from pox.core import core

# import OpenFlow 1.0 module & rename it "of"
import pox.openflow.libopenflow_01 as of

# display message
log = core.getLogger()

# handler function which spesifies what to do when packetIn happens
def _handle_PacketIn (event):

# creating an instruction "msg" for sending packetout
  msg = of.ofp_packet_out()

# specify which data to sent 
  msg.data=event.ofp

# specify flood action
  msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))

# send the instruction to device
  event.connection.send(msg)

# is used for initializing pox component
def launch ():

#specify handler function when PacketIn occurs
  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)

#display message
  log.info("Hub running.")
