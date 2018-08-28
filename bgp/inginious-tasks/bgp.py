# This is an example script to create and run a simple BGP network

from network_manager import *

# EBGTopo is the base class to create a simple eBGP network
topo = EBGPTopo()


# We can add an AS by specifying its AS number and its advertised prefixes
as1 = topo.add_AS(1, ('1111:0:0::/48',))
as2 = topo.add_AS(2, ('2222:0:0::/48',))
as3 = topo.add_AS(3, ('3333:0:0::/48',))
as4 = topo.add_AS(4, ('4444:0:0::/48',))
as5 = topo.add_AS(5, ('5555:0:0::/48',))

# We can connect the ASes using shared cost peering or the provider customer peering
topo.provider_customer_peering(as2, as1)
topo.provider_customer_peering(as1, as4)
topo.shared_cost_peering(as1, as3)
topo.shared_cost_peering(as2, as5)

# The NetworkManager is a usefull class to easily run a virtual network based on
# a topology.
nw = NetworkManager(topo)
nw.start_network()

# Retrieve some information about the network then print it in order to catch 
# the output in SSH
print(nw.get_converged_ribs_per_as())

nw.stop_network()