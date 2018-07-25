import sys
import os
import ipaddr
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../ipmininet'))

import ipmininet
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo
from mininet.log import lg as log
from ipmininet.clean import cleanup
from ipmininet.router import Router
from ipmininet.router.config import BGP, AS,\
                                    ebgp_session, RouterConfig,\
                                    set_community
import ipmininet.router.config.bgp as _bgp


def error(msg):
    print("Error => " + msg)
    exit(1)


class ASTopo(IPTopo):

    def build_topo(self):
        super(ASTopo, self).build()

    def build(self, *args, **kwargs):
        """Do not use this method, it is only needed for compatibility"""
        return

    def add_AS(self, asn, prefixes):
        try:
            n = int(asn)
        except:
            error("Invalid AS number: " + str(asn))
        self._check_prefix(prefixes)
        tmp = self._addRouter_v6('as'+str(n)+'r1', config=(RouterConfig, {
                'daemons': [(BGP, {'address_families': (
                                    _bgp.AF_INET6(networks=prefixes),),
                                    'advertisement_timer': 1,
                                    'hold_time': 9})]}))
        new_as = AS(n, (tmp,))
        self.addOverlay(new_as)
        return new_as

    def provider_customer_connection(self, provider, customer):
        self._connect_ases(provider, customer)
        set_community(self, provider, customer.asn, str(provider.asn) + ':1336')
        set_community(self, customer, provider.asn, str(customer.asn) + ':1338')

    def peer_connection(self, as1, as2):
        self._connect_ases(as1, as2)
        set_community(self, as1, as2.asn, str(as1.asn) + ':1337')
        set_community(self, as2, as1.asn, str(as2.asn) + ':1337')
    
    def _addRouter_v6(self, name, **kwargs):
        return self.addRouter(name, use_v4=False, use_v6=True, **kwargs)

    def _connect_ases(self, as1, as2):
        if as1 == None or as2 == None:
            error("You are trying to make a connection with an inexisting AS!")
        if as1.nodes.count == 0 or as2.nodes.count == 0:
            error("You are trying to connect to an AS without any router.")
        self.addLink(as1.nodes[0], as2.nodes[0])
        ebgp_session(self, as1.nodes[0], as2.nodes[0])

    def _check_prefix(self, prefixes):
        try:
            for p in prefixes:
                l = int(p[p.find("/")+1:])
                ipaddr.IPAddress(p[:p.find("/")])
                if l <= 0 or l >= 128:
                    raise Error()
        except:
            error("Invalid prefixes: " + prefixes)


def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj

class NetworkManager:

    def __init__(self, *args, **kwargs):
        self.RIBCommand = '(echo zebra; echo "show bgp"; sleep 1; exit;) | telnet localhost bgpd'
        self.topo = ASTopo()

    def add_AS(self, asn, prefixes):
        return self.topo.add_AS(asn, prefixes)

    def peer_connection(self, as1, as2):
        self.topo.peer_connection(as1, as2)

    def provider_customer_connection(self, provider, customer):
        self.topo.provider_customer_connection(provider, customer)

    def start_network(self):
        try:
            self.topo.build_topo()
            self.net = IPNet(topo=self.topo, use_v4=False, use_v6=True)
            self.net.start()
        except:
            self.stop_network()
            error('Cannot start the network.')

    def stop_network(self):
        self.net.stop()
        cleanup()

    def get_converged_ribs_per_as(self):
        return self._get_converged(self.get_all_ribs_per_as)

    def get_converged_ribs_per_router(self):
        return self._get_converged(self.get_all_ribs_per_router)

    def get_all_ribs_per_router(self):
        return self._get_all_ribs(lambda r: r.name)

    def get_all_ribs_per_as(self):  
        return self._get_all_ribs(lambda r: 'as'+str(r.asn))

    def get_rib(self, node):
        if not self.net.is_running:
            error("The network is not running.")
        r = self._get_node(node)
        if r not in self.net.routers:
            return None
        out = r.cmd(self.RIBCommand)
        if 'Connection refused' not in out:
            return self._parse_rib(out)
        else:
            return None

    def _get_node(self, node):
        if type(node) is Router:
            return node
        elif type(node) is AS:
            return next(r for r in self.net.routers if r.name == node.nodes[0])
        error("The node is neither a router nor an AS.")

    def _parse_rib(self, out):
        lines = out.split('\n')[19:-5]
        rib = {}
        dest = ''
        m = 0
        for l in lines:
            param = l.split()
            if l[3] is not ' ':
                dest = param[1]
                rib[dest] = {'primary': '', 'secondary': []}
                m = 0
            else:
                m = -1
            if param[4+m] is not '0' and param[4+m] != '32768':
                m = m-1
            if '>' in param[0]:
                rib[dest]['primary'] = ','.join(param[5+m:])
            else:
                rib[dest]['secondary'].append(','.join(param[5+m:]))
        return rib

    def _get_converged(self, f):
        old = f()
        new = ""
        while ordered(new) != ordered(old):
            time.sleep(3)
            old = new
            new = f()
        return new

    def _get_all_ribs(self, f):
        if not self.net.is_running:
            error("The network is not running.")
        ribs = {}
        for r in self.net.routers:
            ribs[f(r)] = self.get_rib(r)
        return ribs
