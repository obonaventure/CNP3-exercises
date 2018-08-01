#!/bin/python3
# -*- coding: utf-8 -*-
#
# This file is part of INGInious. See the LICENSE and the COPYRIGHTS files for
# more information about the licensing of this file.

import sys
import subprocess
from inginious import feedback
from ast import literal_eval

class AS:
    def __init__(self, asn):
        self.asn = "as" + str(asn)
        self.prefix = str(asn)*4+"::/48"

def error(msg):
    feedback.set_global_result("crash")
    feedback.set_global_feedback(msg)
    exit(0)

def upload_file(file):
    r = subprocess.run(["/bin/upload-to-vm", file], stdout=subprocess.PIPE)
    if r.returncode != 0:
        error("Unable to send the file {} to the VM.".format(file))

def execute_file(file):
    r = subprocess.run(["/bin/execute-in-vm", "python {}".format(file)], 
               stdout=subprocess.PIPE)
    if r.returncode != 0:
        error("Unable to execute the file " + file)
    return r.stdout.decode("utf-8")

def get_ribs(file, node=None):
    upload_file(file)
    f = file[file.rfind('/')+1:]
    out = execute_file(f)
    if "Error" in out:
        return None
    ribs = literal_eval(out)
    if node:
        return ribs[node]
    else:
        return ribs

def compare_best_route(answer, rib, prefix):
    if answer == "NONE" and not prefix in rib.keys():
        return True
    elif answer == "NONE":
        return False
    best = ["AS"+str(x) for x in rib[prefix]["primary"].split(",") if x != "i"]
    if len(answer) != len(best):
        return False
    for i, v in enumerate(best):
        if answer[i] != v:
            return False
    return True
 
def compare_all_routes(answer, rib, prefix):
    if answer == "NONE" and not prefix in rib.keys():
        return True
    elif answer == "NONE":
        return False
    routes = [["AS"+str(x) for x in rib[prefix]["primary"].split(",") if x != "i"]]
    for l in rib[prefix]["secondary"]:
        routes.append(["AS"+str(x) for x in l.split(",") if x != "i"])
    if len(answer) != len(routes):
        return False
    for i, r in enumerate(routes):
        for j, v in enumerate(r):
            if answer[i][j] != v:
                return False
    return True

def compare_known_prefixes(answer, rib):
    if len(answer) != len(rib.keys()):
        return False
    for p in rib.keys():
        if p not in answer:
            return False
    return True

