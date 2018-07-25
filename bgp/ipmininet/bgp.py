from scripts import NetworkManager
from ipmininet.cli import IPCLI


nw = NetworkManager()

as1 = nw.add_AS(1, ('1111:0:0::/48',))
as2 = nw.add_AS(2, ('2222:0:0::/48',))
as3 = nw.add_AS(3, ('3333:0:0::/48',))
as4 = nw.add_AS(4, ('4444:0:0::/48',))
as5 = nw.add_AS(5, ('5555:0:0::/48',))

nw.provider_customer_connection(as2, as1)
nw.provider_customer_connection(as1, as4)
nw.peer_connection(as1, as3)
nw.peer_connection(as2, as5)

nw.start_network()

print(nw.get_converged_ribs_per_as())

nw.stop_network()