import time
from scripts import NetworkManager
from ipmininet.cli import IPCLI


g = NetworkManager()

as1 = g.add_AS(1, ('1111:0:0::/48',))
as2 = g.add_AS(2, ('2222:0:0::/48',))
as3 = g.add_AS(3, ('3333:0:0::/48',))
as4 = g.add_AS(4, ('4444:0:0::/48',))
as5 = g.add_AS(5, ('5555:0:0::/48',))

g.provider_customer_connection(as2, as1)
g.provider_customer_connection(as1, as4)
g.peer_connection(as1, as3)
g.peer_connection(as2, as5)

g.start_network()
time.sleep(10)
print(g.get_rib(as1))
print(g.get_all_ribs_per_as())
g.stop_network()