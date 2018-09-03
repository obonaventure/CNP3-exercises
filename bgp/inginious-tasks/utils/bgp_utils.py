import random
from ast import literal_eval
from inginious.vm import vm_utils as vm
from .inginious_utils import get_random, shuffle

class AS:
    """Class to facilitates the manipulation of as number and prefix"""

    def __init__(self, asn, prefix):
        self.asn = asn
        self.prefix = prefix

def parse_bgp_file(filename, fileout):
    """This method parse the file describing a bgp network and write the 
    necessary code to create such a network.
    
    :param filename: the text file describing the network
    :param fileout: the file in which the python code will be written"""

    file = open(filename, 'r')
    desc = file.read().split('\n')
    file.close()

    ases = []
    doshuffle = False
    bgp_string = "from network_manager import *\ntopo = EBGPTopo()\n"
    for line in desc:
        if len(line) == 0:
            continue
        d = line.split(' ')
        if d[0].upper() == 'AS':
            ases.append(AS(d[1], d[2]))
            bgp_string += "{} = topo.add_AS({}, ('{}',))\n".format(d[1], d[1][2:], d[2])
        elif d[0].upper() == 'SHARED_COST':
            bgp_string += "topo.shared_cost_peering({}, {})\n".format(d[1], d[2])
        elif d[0].upper() == 'PROVIDER_CUSTOMER':
            bgp_string += "topo.provider_customer_peering({}, {})\n".format(d[1], d[2])
        elif d[0].upper() == "SHUFFLE":
            doshuffle = True

    bgp_string += ("nw = NetworkManager(topo)\n"
                  "nw.start_network()\n"
                  "print(nw.get_converged_ribs_per_as())\n"
                  "nw.stop_network()\n")
    f = open(fileout, 'w')
    f.write(bgp_string)
    f.close()
    if not doshuffle:
        return ases, None
    return ases, shuffle(ases)

def deshuffle_answer(answer, ordered, shuffled):
    """"This method will match the answer based on a randomized network with
    the network ran in the virtual machine.
    
    :param answer: The answer based on the randomized network
    :param ordered: The list of the ASes, in the same order as ran in the
                    virtual network
    :param shuffled: The list of the ASes, shuffled in the same way as seen
                     by the student"""
    
    if shuffled is None:
        return
    if isinstance(answer[0], list):
        for v in answer:
            deshuffle_answer(v, ordered, shuffled)
        return
    for i, v in enumerate(answer):
        for j, x in enumerate(shuffled):
            if v == x.asn.upper():
                answer[i] = v.replace(x.asn.upper(), ordered[j].asn.upper())
                break
            elif v == x.prefix:
                answer[i] = v.replace(x.prefix, ordered[j].prefix)
                break

def get_ribs(file):
    """This method takes a python script containing code to create and run a
    virtual network using ipmininet, and return the RIB of each node of the 
    network in a dictionnary.
    
    :param file: The python script creating and launching the network"""

    vm.upload_file(file)
    f = file[file.rfind('/')+1:]
    out = vm.execute_command("python {}".format(f))
    if "Error" in out:
        return out
    try:
        return literal_eval(out)
    except:
        return "Error: Unable to parse the output. Is the script correct?"

def compare_best_route(answer, rib, prefix):
    """This method check whether the answer is the best route toward a prefix 
    known by an AS.

    :param answer: The answer to check
    :param rib: The RIB of the AS with which we compare the best route
    :param prefix: The prefix towards which we compare the best route"""

    if answer == "NONE" and not prefix in rib.keys():
        return True
    elif answer == "NONE" or not prefix in rib.keys():
        return False
    best = ["AS"+str(x) for x in rib[prefix]["primary"].split(",") if x != "i"]
    if len(answer) != len(best):
        return False
    for i, v in enumerate(best):
        if answer[i] != v:
            return False
    return True
 
def compare_all_routes(answer, rib, prefix):
    """This method check whether the answer contains all the routes toward a prefix
    known by an AS, and  that it contains no other routes.

    :param answer: The answer to check
    :param rib: The RIB of the AS with which we compare the routes
    :param prefix: The prefix towards which we compare the routes"""

    if answer == "NONE" and not prefix in rib.keys():
        return True
    elif answer == "NONE" or not prefix in rib.keys():
        return False
    routes = [["AS"+str(x) for x in rib[prefix]["primary"].split(",") if x != "i"]]
    for l in rib[prefix]["secondary"]:
        routes.append(["AS"+str(x) for x in l.split(",") if x != "i"])
    if len(answer) != len(routes):
        return False
    for i, r in enumerate(routes):
        if r != answer[i]:
            return False
    return True

def compare_known_prefixes(answer, rib):
    """This method check whether the answer contains all the prefixes known by an
    AS, and that it does not contain any other.

    :param answer: The answer to check
    :param rib: The RIB of the AS with which we compare the prefixes"""

    if len(answer) != len(rib.keys()):
        return False
    for p in rib.keys():
        if p not in answer:
            return False
    return True
