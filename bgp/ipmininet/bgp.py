from scripts import *

topo = EBGPTopo()

as1 = topo.add_AS(1, ('1111:0:0::/48',))
as2 = topo.add_AS(2, ('2222:0:0::/48',))
as3 = topo.add_AS(3, ('3333:0:0::/48',))
as4 = topo.add_AS(4, ('4444:0:0::/48',))
as5 = topo.add_AS(5, ('5555:0:0::/48',))

topo.provider_customer_peering(as2, as1)
topo.provider_customer_peering(as1, as4)
topo.shared_cost_peering(as1, as3)
topo.shared_cost_peering(as2, as5)


nw = NetworkManager(topo)
nw.start_network()

print(nw.get_converged_ribs_per_as())

nw.stop_network()